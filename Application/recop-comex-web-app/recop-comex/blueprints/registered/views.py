from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from blueprints.registered.forms import *
from data_access.models import donation, user_account
from data_access.queries import user_views
from datetime import datetime

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

	return render_template('/registered/events/index.html')

@registered.route('/registered/events/create')
@login_required
def events_create():

	return render_template('/registered/events/create.html')

@registered.route('/registered/linkages')
@login_required
def linkages():

	return render_template('/registered/linkages/index.html')

@registered.route('/registered/donate',methods=['GET', 'POST'])
@login_required
def donate():

	form = DonationForm()

	if form.validate_on_submit():

		id_donation = donation.count()
		id_sponsee = user_account.query.filter_by(id=current_user.id).first()

		values = donation(
			id=id_donation, 
			sponsee_id=id_sponsee.info_id, 
			sponsor_id=0, 
			amount=form.amount.data, 
			date_given=datetime.now(), 
			transaction_slip="asdasdasd", 
			is_event='a', 
			status='N')

		db.session.add(values)
		db.session.commit()

	return render_template('/registered/donate/index.html',form = form)

@registered.route('/registered/contactus')
@login_required
def contactus():

	return render_template('/registered/contactus/index.html')

@registered.route('/registered/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/registered/termsandconditions/index.html')

@registered.route('/registered/profile/about/<user>')
@login_required
def profile_about(user):

	registered = user_views.profile_info(current_user.info_id)

	return render_template('/registered/profile/about.html', registered=registered)

@registered.route('/registered/profile/update/<user>', methods=['GET', 'POST'])
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

			return redirect(url_for('registered.profile_about', user=current_user.username))

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

	return render_template('/registered/profile/update.html', form=form)

@registered.route('/registered/profile/updatepassword/<user>', methods=['GET', 'POST'])
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

			return redirect(url_for('registered.profile_about', user=current_user.username))

		else:

			flash('Wrong password.', 'error')


	return render_template('/registered/profile/update_password.html', form=form)

	