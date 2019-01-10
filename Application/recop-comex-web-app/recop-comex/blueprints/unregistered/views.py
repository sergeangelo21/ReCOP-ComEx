from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user, login_required
from blueprints.unregistered.forms import LoginForm, SignupForm
from data_access.models import user_account, user_information

from datetime import datetime
from extensions import db

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

		value_user_account = [
			id_user_account,id_user_information,form.username.data,
			form.password.data,form.email.data,1,datetime.utcnow(),"A"
			]
		user_account.add(value_user_account)

		value_user_information = [
			id_user_information,form.firstname.data,form.middlename.data,
			form.lastname.data,form.company.data,form.gender.data,
			form.address.data,form.telephone.data,form.mobile.data,form.type.data,"Y"
			]
		user_information.add(value_user_information)

	return render_template('/unregistered/signup.html', form=form)

@unregistered.route('/login', methods=['GET', 'POST'])
def login():

	if current_user.is_authenticated and not current_user.is_anonymous:
		return redirect(url_for(''))

	form = LoginForm()

	if form.validate_on_submit():
        
		user = user_account.query.filter(user_account.username==form.username.data).first()

		if user is None or user.password!=form.password.data:

			flash('Invalid username or password')
			return redirect(url_for('unregistered.login'))

		# else:
            
        #     role = user_role.query.filter(user_role.id==user.role_id).first()
        #     session['role']=role.id

		login_user(user, remember=form.remember_me.data)

        # if session['role']==1:
        #     return redirect(url_for('backend.dashboard'))
        # elif session['role']==2:
        #     return redirect(url_for('admin_hospital.dashboard'))
        # elif session['role']==6:
        #     return redirect(url_for('onevents.onevent'))
        # else:
		return redirect(url_for('registered.index'))

	return render_template('/unregistered/login.html', form=form)

@unregistered.route('/logout')
def logout():

	last_active = user_account.query.filter_by(id=current_user.id).first()
	last_active.last_active = datetime.now()

	db.session.commit()

	logout_user()

	return redirect('/')