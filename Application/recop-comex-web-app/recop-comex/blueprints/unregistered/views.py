from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from blueprints.unregistered.forms import LoginForm, SignupForm
from blueprints.unregistered.checker import authenticate
from data_access.models import user_account, user_information

from datetime import datetime

import os

unregistered = Blueprint('unregistered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@unregistered.route('/')
def index():

	check = authenticate()
	
	if check:
		return check

	return render_template('/unregistered/index.html')

@unregistered.route('/events')
def events():

	check = authenticate()
	
	if check:
		return check

	return render_template('/unregistered/events.html')

@unregistered.route('/partners')
def partners():

	check = authenticate()
	
	if check:
		return check

	return render_template('/unregistered/partners.html')

@unregistered.route('/contactus')
def contactus():

	check = authenticate()
	
	if check:
		return check

	return render_template('/unregistered/contactus.html')

@unregistered.route('/signup', methods=['GET', 'POST'])
def signup():

	check = authenticate()
	
	if check:
		return check

	form = SignupForm()

	if form.validate_on_submit():

		id_information = user_information.count()
		id_account = user_account.count()

		value_information = [
			id_information,form.firstname.data,form.middlename.data,
			form.lastname.data,form.company.data,form.gender.data,
			form.address.data,form.telephone.data,form.mobile.data,form.type.data
			]

		user_information.add(value_information)

		if int(form.type.data) > 0:
			status = "D"
		else:
			status = "A"

		value_account = [
			id_account,id_information,form.username.data,
			form.password.data,form.email.data,form.type.data,datetime.utcnow(),status
			]
		user_account.add(value_account)


	return render_template('/unregistered/signup.html', form=form)

@unregistered.route('/login', methods=['GET', 'POST'])
def login():

	check = authenticate()
	
	if check:
		return check

	form = LoginForm()

	if form.validate_on_submit():
        
		user = user_account.login([form.username.data, form.password.data])

		if user is None:
			flash('Invalid username or password')
			return redirect(url_for('unregistered.login'))

		login_user(user, remember=form.remember_me.data)

		if current_user.type == 2:	
			return redirect(url_for('linkages.index'))
	
	return render_template('/unregistered/login.html', form=form)

@unregistered.route('/logout')
def logout():

	user_account.logout()

	logout_user()

	return redirect('/')