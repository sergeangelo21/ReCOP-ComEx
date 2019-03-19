from flask import Flask, Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, logout_user, login_required
from blueprints.registered.forms import *
from data_access.models import donation, user_account, user_information, event_information, event_participation, event_attachment, donation, user_photo
from data_access.queries import user_views, linkage_views, event_views, donation_views
from datetime import datetime

from extensions import db, bcrypt
import os


registered = Blueprint('registered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@registered.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))
		elif current_user.type == 5:
			return redirect(url_for('religious_admin.index'))
		user_account.logout()

@registered.route('/registered')
@login_required
def index():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/registered/index.html', photo=photo, active='home')

@registered.route('/registered/events/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
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

	events = event_views.registered_events([value, search, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	user = event_participation.user_joined(current_user.info_id)

	if form.validate_on_submit():

		return redirect(url_for('registered.events', status=status, page='1', search=form.search.data))

	return render_template('/registered/events/index.html', title="Events", form=form, events=events, user=user, status=status, search=search, photo=photo, active='events')

@registered.route('/registered/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	photo = user_photo.photo(current_user.info_id)

	events = event_information.calendar()
	
	return render_template('/registered/events/index-calendar.html', title="Events", events=events, photo=photo, active='events')

@registered.route('/registered/events/<action>/id=<id>')
@login_required
def event_action(id, action):

	event = event_views.show_info(id)
	status = event_participation.show_status([id, current_user.info_id])

	if action == 'join':

		if status:

			value = [event.id, current_user.info_id, 'J']

			event_participation.update(value)

			flash('Successfully	 joined '+event.name, 'success')

		else:

			value = [None, id, current_user.info_id, 'N']

			event_participation.add(value)

			flash('Successfully	 joined '+event.name, 'success')

	else:

		value = [event.id, current_user.info_id, 'C']

		event_participation.update(value)

		flash('Participation has been cancelled!', 'success')

	return redirect(url_for('registered.events', status='all', page='1', search=' '))

@registered.route('/registered/linkages/search_<search>.page_<page>', methods=['GET','POST'])
@login_required
def linkages(page, search):

	linkages = linkage_views.show_list(['A', search, 3, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('registered.linkages', page='1', search=form.search.data))

	return render_template('/registered/linkages/index.html', title="linkages", form=form, linkages=linkages, page=page, search=search, photo=photo, active='linkages')

@registered.route('/registered/communities/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def communities(page, search):

	communities = linkage_views.show_list(['all',search,4, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('registered.communities', page='1', search=form.search.data))

	return render_template('/registered/communities/index.html', form=form, communities=communities, search=search, photo=photo, active='communities')

@registered.route('/registered/donate', methods=['GET', 'POST'])
@login_required
def donate():

	photo = user_photo.photo(current_user.info_id)

	form = DonationForm()

	donations = donation_views.donation_history(current_user.info_id)

	communities = linkage_views.target_linkages()

	for c in communities:

		if c.type==4:
			form.sponsee.choices.extend([(str(c.id), c.address)])

	events = event_information.select_list()

	if events:

		for e in events:
			form.event.choices.append((str(e.id), e.name))
			no_event = 0

	else: 
		
		form.event.data=''
		no_event = 1

	if form.validate_on_submit():

		if form.give_to.data=='1':
			if form.sponsee.data:
				sponsee = form.sponsee.data
			else:
				sponsee = 1

			event = None
		else:
			event = form.event.data
			sponsee= None

		file = form.trans_slip.data
		old, extension = os.path.splitext(file.filename)

		new = donation.last_added()
		filename = str(new)+extension

		trans_path = 'static/output/donate/trans_slip/' + filename

		value = [None,sponsee,event,current_user.info_id,form.amount.data,trans_path,'N']

		donation.add(value)
		file.save(trans_path)

		flash('Donation given!', 'success')
		return redirect(url_for('registered.donate'))

	return render_template('/registered/donate/index.html', form=form, no_event=no_event, donations=donations, photo=photo, active='donate')

@registered.route('/registered/referral', methods=['GET', 'POST'])
@login_required
def referral_users():

	photo = user_photo.photo(current_user.info_id)

	form = ReferralForm()

	if form.validate_on_submit():

		html = 'asdlkfjasfd'
		subject = 'REFFERAL: '
		admin = user_account.query.by(id=1).first()

		email_parts = [html, subject, admin.email_address, form.email.data, None]
		send_email(email_parts)

		value = [None, current_user.id, form.name.data, form.email.data, form.type.data, 'N']

		referral.add(value)

		flash('Referral has been sent!', 'success')
		return redirect(url_for('registered.referral_users'))

	return render_template('/registered/referral/index.html', form=form, photo=photo, active='referral')

@registered.route('/registered/contactus')
@login_required
def contactus():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/registered/contactus/index.html', photo=photo, active='contactus')

@registered.route('/registered/termsandconditions')
@login_required
def termsandconditions():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/registered/termsandconditions/index.html', photo=photo, active='termsandconditions')

@registered.route('/registered/profile/about|<user>', methods=['GET', 'POST'])
@login_required
def profile_about(user):

	registered = user_views.profile_info(current_user.info_id)
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
		return redirect(url_for('registered.profile_about', user=user))

	return render_template('/registered/profile/about.html', title="registered", registered=registered, photo=photo, form=form, active='about')

@registered.route('/registered/profile/eventsattended|<user>')
@login_required
def profile_eventsattended(user):

	photo = user_photo.photo(current_user.info_id)
	
	return render_template('/registered/profile/eventsattended.html', title="registered", photo=photo, active='eventsattended')	

@registered.route('/registered/profile/settings/personal|<user>', methods=['GET', 'POST'])
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

		return redirect(url_for('registered.profile_settings_personal', user=current_user.username))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/registered/profile/settings/personal.html', form=form, photo=photo)

@registered.route('/registered/profile/settings/contact|<user>', methods=['GET', 'POST'])
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

		return redirect(url_for('registered.profile_settings_contact'), user=current_user.username)

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/registered/profile/settings/contact.html', form=form)	

@registered.route('/registered/profile/settings/username|<user>', methods=['GET', 'POST'])
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

			return redirect(url_for('registered.profile_settings_username', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/registered/profile/settings/username.html', form=form)

@registered.route('/registered/profile/settings/password|<user>', methods=['GET', 'POST'])
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

			return redirect(url_for('registered.profile_settings_password', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	return render_template('/registered/profile/settings/password.html', form=form)

@registered.route('/logout/registered')
def logout():

	user_account.logout()

	logout_user()

	flash('You are logged out.', 'success')

	return redirect('/')