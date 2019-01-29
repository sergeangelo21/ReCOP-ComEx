from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from blueprints.registered.forms import *
from data_access.models import *

from extensions import db, bcrypt
import os

registered = Blueprint('registered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@registered.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('beneficiaries.index'))
		elif current_user.type == 1:
			return redirect(url_for('admin.index'))

@registered.route('/registered')
@login_required
def index():

	return render_template('/registered/index.html')

@registered.route('/registered/events')
@login_required
def events():

	return render_template('/registered/events/_events.html')

@registered.route('/registered/events/create')
@login_required
def events_create():

	return render_template('/registered/events/create.html', )

@registered.route('/registered/partners')
@login_required
def partners():

	return render_template('/registered/partners.html')

@registered.route('/registered/donate')
@login_required
def donate():

	return render_template('/registered/donate.html')

@registered.route('/registered/contactus')
@login_required
def contactus():

	return render_template('/registered/contactus.html')

@registered.route('/registered/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/registered/termsandconditions.html')

@registered.route('/registered/profile/<registered>')
@login_required
def profile(registered):

	registered = user_information.query.join(
		user_account
		).add_columns(
		user_information.first_name,
		user_information.middle_name,
		user_information.last_name,
		user_information.company_name,
		user_information.bio,
		user_information.gender,
		user_information.birthday,
		user_information.address,
		user_information.address,
		user_information.telephone,
		user_information.mobile_number,
		user_account.username,
		user_account.password,
		user_account.email_address
		).filter_by(id=current_user.id).first()

	return render_template('/registered/profile/profile.html', registered=registered)

@registered.route('/registered/profile/update/<registered>', methods=['GET', 'POST'])
@login_required
def profile_update(registered):

	user_information_update = user_information.query.filter_by(id=current_user.id).first()
	user_account_update = user_account.query.filter_by(id=current_user.id).first()

	form = ProfileUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

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
			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			return redirect(url_for('registered.profile', registered=current_user.username))

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
		form.password.data = user_account_update.password

	return render_template('/registered/profile/profile_update.html', form=form, user_account=registered)