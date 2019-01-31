from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from blueprints.beneficiaries.forms import *
from data_access.models import user_account, user_information, proposal_tracker, event_information
from data_access.queries import user_views

from extensions import db, bcrypt
import os

beneficiaries = Blueprint('beneficiaries', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@beneficiaries.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))

@beneficiaries.route('/beneficiaries')
@login_required
def index():

	return render_template('/beneficiaries/index.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/events')
@login_required
def events():

	events = event_information.query.all()

	return render_template('/beneficiaries/events/index.html', title="Beneficiaries", events=events)

@beneficiaries.route('/beneficiaries/reports')
@login_required
def reports():

	return render_template('/beneficiaries/reports.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/contactus')
@login_required
def contactus():

	return render_template('/beneficiaries/contactus.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/beneficiaries/termsandconditions.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/profile/about/<user>')
@login_required
def profile_about(user):

	beneficiaries = user_views.profile_info(current_user.info_id)

	return render_template('/beneficiaries/profile/about.html', title="Beneficiaries", beneficiaries=beneficiaries)

@beneficiaries.route('/beneficiaries/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/beneficiaries/profile/eventsattended.html', title="Beneficiaries")	

@beneficiaries.route('/beneficiaries/profile/settings')
@login_required
def profile_settings():

	return render_template('/beneficiaries/profile/settings.html', title="Beneficiaries")	

@beneficiaries.route('/beneficiaries/profile/update/<user>', methods=['GET', 'POST'])
@login_required
def profile_update(user):

	user_information_update = user_views.profile_info_update(current_user.info_id)
	user_account_update = user_views.profile_acc_update(current_user.info_id)

	form = ProfileUpdateForm()

	if form.validate_on_submit():

		if user:

			user_information_update.first_name = form.firstname.data
			user_information_update.middle_name = form.middlename.data
			user_information_update.last_name = form.lastname.data
			user_information_update.gender = form.gender.data
			user_information_update.birthday = form.birthday.data
			user_information_update.bio = form.bio.data

			user_information_update.company_name = form.company.data
			user_information_update.address = form.address.data
			user_information_update.telephone = form.telephone.data
			user_information_update.mobile_number = form.mobile.data

			db.session.commit()

			user_account_update.email_address = form.email.data

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Profile was successfully updated!', 'success')

			return redirect(url_for('beneficiaries.profile_about', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio
		
		form.company.data = user_information_update.company_name
		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

		form.username.data = user_account_update.username

	return render_template('/beneficiaries/profile/update.html', form=form)

@beneficiaries.route('/beneficiaries/profile/updatepassword/<user>', methods=['GET', 'POST'])
@login_required
def profile_update_password(user):

	user_account_update = user_views.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('beneficiaries.profile_about', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	return render_template('/beneficiaries/profile/update_password.html', form=form)