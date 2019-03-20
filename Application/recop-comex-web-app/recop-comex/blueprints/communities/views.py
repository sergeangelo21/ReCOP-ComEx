from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, logout_user, login_required
from blueprints.communities.forms import *
from data_access.models import user_account, user_information, proposal_tracker, event_information, community_member, community_info, event_participation, referral, event_attachment, user_photo
from data_access.queries import user_views, linkage_views, community_views, event_views

from static.email import send_email
from extensions import db, bcrypt
from datetime import datetime

import os

communities = Blueprint('communities', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@communities.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 5:
			return redirect(url_for('religious_admin.index'))
		user_account.logout()
		
@communities.route('/communities')
@login_required
def index():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/communities/index.html', title="Home", photo=photo, active='home')

@communities.route('/communities/events/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def events(status, page, search):

	if status=='scheduled':
		value='S'
	elif status=='new':
		value='N'
	elif status=='finished':
		value='F'
	else:
		value=status

	events = event_views.community_events([value, search, page, current_user.info_id])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('communities.events', status=status, page='1', search=form.search.data))

	return render_template('/communities/events/index.html', title="Events", form=form, events=events, status=status, search=search, photo=photo, active='events')

@communities.route('/communities/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	photo = user_photo.photo(current_user.info_id)

	events = event_information.calendar()
	
	return render_template('/communities/events/index-calendar.html', title="Events", events=events, photo=photo, active='events')
	
@communities.route('/communities/events/show/id=<id>')
@login_required
def event_participants(id):

	event = event_views.show_info(id)
	participants = community_views.event_participants(id)
	joined = event_participation.show_joined(id)

	form = SearchForm()

	return render_template('/communities/events/add_participants.html', title= event.name.title() , event = event, participants=participants, joined=joined, form=form, active='events')

@communities.route('/communities/event_<id>/<action>/<participant>')
@login_required
def participant_action(id, action, participant):

	if action=='add':

		record = event_participation.show_status([id, participant])

		if record is None:
			value = [None, id, participant, 'N']
			event_participation.add(value)
		else:
			value = [id, participant, 'J']
			event_participation.update(value)

		flash('Member added to event!', 'success')

	elif action=='remove':

		value = [id, participant, 'R']
		event_participation.update(value)
		flash('Member removed from event!', 'success')

	return redirect(url_for('communities.event_participants',id=id))

@communities.route('/communities/members/search_<search>', methods=['GET', 'POST'])
@login_required
def members(search):

	members = community_views.members_list(search)

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('communities.members', search=form.search.data))

	return render_template('/communities/members/index.html', title="Members", members=members, form=form, search=search, photo=photo,  active='members')

@communities.route('/communities/members/add', methods=['GET', 'POST'])
@login_required
def member_add():

	form = AddMemberForm()

	if form.validate_on_submit():

		for_company = user_views.profile_info(current_user.info_id)

		value = [
			None,form.firstname.data, form.middlename.data, form.lastname.data, 
			for_company.company_name, None, form.gender.data, form.birthday.data,
			form.address.data, form.telephone.data, form.mobile.data, 0
			]

		user_information.add(value)

		user_id = user_information.reserve_id()

		if form.occupation.data=='':
			occupation=None
		else:
			occupation=form.occupation.data

		value = [None, user_id, current_user.info_id, occupation, form.income.data, form.religion.data, "A"]

		community.add(value)

		flash('Member added!', 'success')
		return redirect(url_for('communities.members', search=' '))

	return render_template('/communities/members/add.html', title="Add Member", form=form, active='members')

@communities.route('/communities/members/update/id=<id>', methods=['GET', 'POST'])
@login_required
def member_updateinfo(id):

	user = community.retrieve_member(id)
	member = user_information.linkage_info(user.member_id)

	form = UpdateMemberForm()

	if form.validate_on_submit():

		member.first_name = form.firstname.data
		member.middle_name = form.middlename.data
		member.last_name = form.lastname.data
		member.gender = form.gender.data
		member.birthday = form.birthday.data
		user.occupation = form.occupation.data
		user.income = form.income.data
		user.religion = form.religion.data
		member.address = form.address.data
		member.telephone = form.telephone.data
		member.mobile_number = form.mobile.data

		db.session.commit()

		flash('Member updated!', 'success')

		return redirect(url_for('communities.members', search=' '))

	else:

		form.firstname.data = member.first_name
		form.middlename.data = member.middle_name
		form.lastname.data = member.last_name
		form.gender.data = member.gender
		form.birthday.data = member.birthday
		form.occupation.data = user.occupation
		form.income.data = user.income
		form.religion.data = user.religion
		form.address.data = member.address
		form.telephone.data = member.telephone
		form.mobile.data = member.mobile_number

	return render_template('/communities/members/update.html', title="Update Member", form=form, active='members')

@communities.route('/communities/members/action/id=<id>')
@login_required
def member_action(id):

	user = community.retrieve_member(id)
	member = user_information.linkage_info(user.member_id)

	if user.status == "A":

		status = "D"
		flash(member.first_name.title() + " was disabled!", "success")

	elif user.status == "D":

		status = "A"
		flash(member.first_name.title() + " was activated!", "success")

	community.update_status(user.id, status)

	return redirect(url_for('communities.members', search=' '))

@communities.route('/communities/linkages/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def linkages(page, search):

	linkages = linkage_views.show_list(['A', search, 3, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('communities.linkages', page='1', search=form.search.data))

	return render_template('/communities/linkages/index.html', title="Linkages", form=form, linkages=linkages, page=page, search=search, photo=photo, active='linkages')

@communities.route('/communities/communities/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def communities_show(page, search):

	communities = linkage_views.show_list(['A',search, 4, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('communities.communities_show', page='1', search=form.search.data))

	return render_template('/communities/communities/index.html', title="Communities", form=form, communities=communities, search=search, photo=photo, active='communities')

@communities.route('/communities/referral', methods=['GET', 'POST'])
@login_required
def referral_users():

	form = ReferralForm()

	if form.validate_on_submit():

		html = 'asdlkfjasfd'
		subject = 'REFFERAL: '
		admin = user_account.retrieve_user(1)

		email_parts = [html, subject, admin.email_address, form.email.data, None]
		send_email(email_parts)

		value = [None, current_user.id, form.name.data, form.email.data, form.type.data, 'N']

		referral.add(value)

		flash('Referral has been sent!', 'success')
		return redirect(url_for('communities.referral_users'))	

	return render_template('/communities/referral/index.html', title="Referral", form=form)

@communities.route('/communities/contactus')
@login_required
def contactus():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/communities/contactus/index.html', title="Contact Us", photo=photo)

@communities.route('/communities/termsandconditions')
@login_required
def termsandconditions():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/communities/termsandconditions/index.html', title="Terms and Conditions", photo=photo)

@communities.route('/communities/profile/about|<user>', methods=['GET', 'POST'])
@login_required
def profile_about(user):

	communities = user_views.profile_info(current_user.info_id)
	photo = user_photo.photo(current_user.info_id)
	form = PictureForm()

	if form.validate_on_submit():

		file = form.photo.data
		old, extension = os.path.splitext(file.filename)
		filename = str(current_user.info_id)+extension
		file_path = 'static/photos/profiles/' + filename

		file.save(file_path)

		if photo:
			user_photo.update([current_user.info_id, file_path])
		else:
			user_photo.add([None, current_user.info_id, file_path])

		flash('Profile picture has been updated!', 'success')
		return redirect(url_for('communities.profile_about', user=user))

	return render_template('/communities/profile/about.html', title="Profile",  photo=photo, form=form, communities=communities)

@communities.route('/communities/profile/eventsattended|<user>')
@login_required
def profile_eventsattended(user):

	photo = user_photo.photo(current_user.info_id)

	return render_template('/communities/profile/eventsattended.html', title="Profile", photo=photo)	

@communities.route('/communities/profile/settings/personal|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_personal(user):

	user_information_update = user_information.profile_info_update(current_user.info_id)

	photo = user_photo.photo(current_user.info_id)

	form = ProfilePersonalUpdateForm()

	if form.validate_on_submit():

		user_information_update.first_name = form.firstname.data
		user_information_update.middle_name = form.middlename.data
		user_information_update.last_name = form.lastname.data
		user_information_update.gender = form.gender.data
		user_information_update.birthday = form.birthday.data
		user_information_update.bio = form.bio.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('communities.profile_settings_personal', user=current_user.username))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/communities/profile/settings/personal.html', title="Update", form=form, photo=photo)

@communities.route('/communities/profile/settings/contact|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_contact(user):

	user_information_update = user_information.profile_info_update(current_user.info_id)
	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileContactUpdateForm()

	if form.validate_on_submit():

		user_information_update.address = form.address.data
		user_information_update.telephone = form.telephone.data
		user_information_update.mobile_number = form.mobile.data

		db.session.commit()

		user_account_update.email_address = form.email.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('communities.profile_settings_contact', user=current_user.username))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/communities/profile/settings/contact.html', title="Update", form=form)	

@communities.route('/communities/profile/settings/username|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_username(user):

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('communities.profile_settings_username', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/communities/profile/settings/username.html', title="Update", form=form)

@communities.route('/communities/profile/settings/password|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_password(user):

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('communities.profile_settings_password', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	return render_template('/communities/profile/settings/password.html', title="Update", form=form)

@communities.route('/logout/communities')
@login_required
def logout():

	user_account.logout()

	logout_user()

	flash('You are logged out.', 'success')

	return redirect('/')
