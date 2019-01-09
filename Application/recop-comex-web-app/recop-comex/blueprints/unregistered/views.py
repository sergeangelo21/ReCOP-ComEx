from flask import Blueprint, render_template
from blueprints.unregistered.forms import LoginForm, SignupForm
from data_access.models import user_account, user_information

from datetime import datetime

import os

unregistered = Blueprint('unregistered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@unregistered.route('/')
def index():

	return render_template('/unregistered/index.html')

@unregistered.route('/events')
def events():

	return render_template('/unregistered/events.html')

@unregistered.route('/partners')
def partners():

	return render_template('/unregistered/partners.html')

@unregistered.route('/contactus')
def contactus():

	return render_template('/unregistered/contactus.html')

@unregistered.route('/signup', methods=['GET', 'POST'])
def signup():

	form = SignupForm()

	if form.validate_on_submit():
		id_user_account = user_account.count()
		id_user_information = user_information.count()

		value_user_account = [id_user_account,id_user_information,form.username.data,form.password.data,form.email.data,"X",datetime.utcnow(),"A"]
		user_account.add(value_user_account)

		value_user_information = [id_user_information,form.firstname.data,form.middlename.data,form.lastname.data,form.gender.data,form.address.data,form.telephone.data,form.mobile.data,"X","Y"]
		user_information.add(value_user_information)

	return render_template('/unregistered/signup.html', form=form)

@unregistered.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated and not current_user.is_anonymous:
		return redirect(url_for(''))

	form = LoginForm()

	return render_template('/unregistered/login.html')