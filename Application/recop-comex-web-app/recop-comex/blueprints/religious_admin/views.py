from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from blueprints.religious_admin.forms import *
from data_access.models import user_account, user_information, audit_trail, proposal_tracker, event_information, event_attachment, donation, user_photo
from data_access.queries import user_views, event_views, linkage_views
from datetime import datetime

from static.email import confirm, generate, send_email
from extensions import db, bcrypt

import os, json, random, string

religious_admin = Blueprint('religious_admin', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@religious_admin.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))

@religious_admin.route('/religious_admin')
@login_required
def index():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/religious_admin/index.html', active='home', photo=photo)

@religious_admin.route('/religious_admin/events/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
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

	events = event_views.religious_admin_events([value, search, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('religious_admin.events', status=status, page='1', search=form.search.data))

	return render_template('/religious_admin/events/index.html', title="Events", form=form, events=events, status=status, search=search, active='events', photo=photo)

@religious_admin.route('/religious_admin/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	events = event_information.calendar()
	
	photo = user_photo.photo(current_user.info_id)

	return render_template('/religious_admin/events/index-calendar.html', title="Events", events=events, active='events', photo=photo)
	
@religious_admin.route('/religious_admin/linkages/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def linkages(page, search):

	linkages = linkage_views.show_list(['A', search, 3, page])

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('religious_admin.linkages', page='1', search=form.search.data))

	return render_template('/religious_admin/linkages/index.html', title="Communities", form=form, linkages=linkages, page=page, search=search, active='linkages')

@religious_admin.route('/religious_admin/communities/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def communities(page, search):

	communities = linkage_views.show_list(['A', search, 4, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('religious_admin.communities', page='1', search=form.search.data))

	return render_template('/religious_admin/communities/index.html', form=form, communities=communities, search=search, active='communities', photo=photo)

@religious_admin.route('/religious_admin/profile/about|<user>' , methods=['GET', 'POST'])
@login_required
def profile_about(user):

	religious_admin = user_views.profile_info(current_user.info_id)
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
		return redirect(url_for('religious_admin.profile_about', user=user))

	return render_template('/religious_admin/profile/about.html', title="religious_admin",  photo=photo, form=form, religious_admin=religious_admin)

@religious_admin.route('/religious_admin/profile/settings/personal|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_personal(user):

	user_information_update = user_information.profile_info_update(current_user.id)

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

		return redirect(url_for('religious_admin.profile_settings_personal', user=user))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/religious_admin/profile/settings/personal.html', title="religious_admin", form=form, photo=photo)

@religious_admin.route('/religious_admin/profile/settings/contact|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_contact(user):

	user_information_update = user_information.profile_info_update(current_user.id)
	user_account_update = user_account.profile_acc_update(current_user.id)

	form = ProfileContactUpdateForm()

	if form.validate_on_submit():

		user_information_update.address = form.address.data
		user_information_update.telephone = form.telephone.data
		user_information_update.mobile_number = form.mobile.data

		db.session.commit()

		user_account_update.email_address = form.email.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('religious_admin.profile_settings_contact', user=user))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/religious_admin/profile/settings/contact.html', title="religious_admin", form=form)	

@religious_admin.route('/religious_admin/profile/settings/username|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_username(user):

	user_account_update = user_account.profile_acc_update(current_user.id)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user_val = user_account.login([current_user.username, form.oldpassword.data])

		if user_val:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('religious_admin.profile_settings_username', user=user))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/religious_admin/profile/settings/username.html', title="religious_admin", form=form)

@religious_admin.route('/religious_admin/profile/update/password|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_password(user):

	user_account_update = user_account.profile_acc_update(current_user.id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user_val = user_account.login([current_user.username, form.oldpassword.data])

		if user_val:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('religious_admin.profile_settings_password', user=user))

		else:

			flash('Wrong password.', 'error')

	return render_template('/religious_admin/profile/settings/password.html', form=form)

@religious_admin.route('/logout/religious_admin')
@login_required
def logout():

	user_account.logout()

	logout_user()

	flash('You are logged out.', 'success')

	return redirect('/')