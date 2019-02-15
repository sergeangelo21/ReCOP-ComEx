from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from blueprints.unregistered.forms import *
from data_access.models import user_account, user_information, audit_trail, proposal_tracker, event_information, event_attachment, donation
from data_access.queries import user_views, event_views, linkage_views
from datetime import datetime

from static.email import confirm, generate, send_email, send_email_resetpassword
from extensions import db, bcrypt

import os, json, random, string

unregistered = Blueprint('unregistered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@unregistered.route('/')
def index():

	return render_template('/unregistered/index.html')

@unregistered.route('/events')
def events():

	events = event_views.show_list('all', ' ')

	return render_template('/unregistered/events/index.html', events=events)

@unregistered.route('/linkages')
def linkages():

	linkages = linkage_views.show_list('A', 3, ' ')

	return render_template('/unregistered/linkages/index.html', linkages=linkages)

@unregistered.route('/donate', methods=['GET', 'POST'])
def donate():

	form=DonationForm()

	communities = linkage_views.target_linkages()

	for c in communities:

		if c.type==4:
			form.sponsee.choices.append((str(c.id), c.address))

	events = event_views.show_list('S', ' ')

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

		value = [None,sponsee,event,1,form.amount.data,trans_path]

		donation.add(value)
		file.save(trans_path)

		flash('Donation given!', 'success')
		return redirect('/')

	return render_template('/unregistered/donate/index.html', form=form, no_event=no_event)

@unregistered.route('/contactus')
def contactus():

	return render_template('/unregistered/contactus/index.html')

@unregistered.route('/signup', methods=['GET', 'POST'])
def signup():

	form = SignupForm()

	if form.validate_on_submit():

		value = [
			None,form.firstname.data,form.middlename.data,
			form.lastname.data,form.company.data,form.bio.data,form.gender.data,form.birthday.data,
			form.address.data,form.telephone.data,form.mobile.data,form.thrust.data
			]

		user_information.add(value)	
		user_id = user_information.reserve_id()

		if form.type.data == '2': 
			status = "A"
			flash('Your account was successfully created!', 'success')
		elif form.type.data == '3' or form.type.data == '4':
			status = "N"
			if form.address.data == 'San Sebastian College Recoletos de Cavite':
				flash('Your account has been created! Please wait for the Re-COP Director to confirm your account.', 'success')
			else:
				flash('Your account has been created! Please wait for MOA at your email.', 'success')

		value = [
			None,user_id,form.username.data,
			form.password.data,form.email.data,form.type.data,datetime.now(),status
			]

		user_account.add(value)

		return redirect(url_for('unregistered.login'))


	return render_template('/unregistered/signup/index.html', form=form)

@unregistered.route('/login', methods=['GET', 'POST'])
def login():

	form = LoginForm()

	if form.validate_on_submit():
        
		user = user_account.login([form.username.data, form.password.data])

		if user is None or user.type==5:
			flash('Invalid username or password', 'error')
			return redirect(url_for('unregistered.login'))

		if user.status != "A":

			if user.status=="P":
				flash('MOA not yet acknowledged. Please check your email.', 'info')
			else:
				flash('Inactive account. Please contact the Re-COP Director.', 'error')
			
			return redirect(url_for('unregistered.login'))

		login_user(user, remember=form.remember_me.data)

		name = user_views.login_info(current_user.id)

		if current_user.type == 3:
			name = name.company_name
		else:
			name = name.first_name
			
		flash('Welcome ' + name + '!', 'success')

		if current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))
		elif current_user.type == 1:
			return redirect(url_for('admin.index'))	
	
	return render_template('/unregistered/login/index.html', form=form)

@unregistered.route('/login/forgotpassword', methods=['GET', 'POST'])
def forgot_password():

	form = ForgotPasswordForm()

	if form.validate_on_submit():

		email = form.email.data
		value = user_account.query.filter_by(email_address=email).first()
		
		if value:
			token = ''.join(random.choice(string.ascii_uppercase + string.digits)for _ in range(6))

			value.password = bcrypt.generate_password_hash(token).decode('utf-8')

			db.session.commit()

			html = 'asdf'
			subject = 'RESET PASSWORD: '
			admin = user_account.query.filter_by(id=1).first()

			email_parts = [token, subject, admin.email_address, email]
			send_email_resetpassword(email_parts)

			flash('Password has been reset. Please check your email.', 'success')
			return redirect(url_for('unregistered.forgot_password'))

		else:

			flash('Email not existing.', 'error')

	return render_template('/unregistered/login/forgot_password.html', form=form)

@unregistered.route('/logout')
def logout():

	user_account.logout()

	logout_user()

	flash('You are logged out.', 'success')

	return redirect('/')

@unregistered.route('/linkages/<token>')
def confirm_linkage(token):

	id = confirm(token)

	if id=='bad':
		flash('Link already expired. Please contact the ReCOP Administrator.', 'error')
		return redirect(url_for('unregistered.index'))

	status = 'A'

	user = user_account.retrieve_user(id)

	if id and user.status=='P':
		
		user_account.update_status(id, status)

		value = [None,id,id,'partner',2]
		audit_trail.add(value)

		flash("MOA acknowledged! Your account is now active.", 'success')

	else:
		
		flash("MOA already acknowledged. Please login.", 'info')
	
	return redirect(url_for('unregistered.login'))

@unregistered.route('/signing/<action>/<token>', methods=['GET', 'POST'])
def event_signing(token, action):

	id = confirm(token)

	if id=='bad':
		flash('Link already expired. Please contact the ReCOP Administrator.', 'error')
		return redirect(url_for('unregistered.index'))

	event = event_views.show_info(id)
	organizer = user_information.linkage_info(event.organizer_id)

	form = LoginForm()

	if form.validate_on_submit():

		user = user_account.login([form.username.data, form.password.data])

		if user and user.type==5:

			if action=='approve':

				if event.status=='A':
					if user.id==4:
						signatory = user_views.signatory_info(3)
						status='F'
					else:
						flash('Invalid credentials! Please try again.', 'error')	
						return redirect(url_for('unregistered.event_signing', token=token, action=action))
				elif event.status=='F':
					if user.id==3:
						signatory = user_views.signatory_info(2)
						status='P'
					else:
						flash('Invalid credentials! Please try again.', 'error')	
						return redirect(url_for('unregistered.event_signing', token=token, action=action))
				elif event.status=='P':
					if user.id==2:
						status='S'
						event_information.update_status(event.id, status)
					else:
						flash('Invalid credentials! Please try again.', 'error')
						return redirect(url_for('unregistered.event_signing', token=token, action=action))	

				proposal_tracker.update_status(event.id, status)

				value = [None,user.id,event.id,'event', 5]
				audit_trail.add(value)

				if status!='S':

					recipient = signatory.email_address
					name = 'Fr. ' + signatory.last_name + ', OAR'
					token = generate(event.id)
					approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
					decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
					html = render_template('admin/email/event.html', event=event , organizer=organizer.company_name, user=name, link = [approve, decline])
					subject = "NEW EVENT: " + event.name
					attachments = event_attachment.retrieve_files(id)

					email_parts = [html, subject, user.email_address, recipient, attachments]

					send_email(email_parts)

				flash(event.name.title() + ' was approved!', 'success')
				return redirect('/')

			else:

				if event.status=='A':
					if user.id!=4:
						flash('Invalid credentials! Please try again.', 'error')	
						return redirect(url_for('unregistered.event_signing', token=token, action=action))
				elif event.status=='F':
					if user.id!=3:
						flash('Invalid credentials! Please try again.', 'error')	
						return redirect(url_for('unregistered.event_signing', token=token, action=action))
				elif event.status=='P':
					if user.id!=2:
						flash('Invalid credentials! Please try again.', 'error')
						return redirect(url_for('unregistered.event_signing', token=token, action=action))

				status='X'
				proposal_tracker.update_status(event.id, status)
				event_information.update_status(event.id, status)

				value = [None,user.id,event.id,'event', 6]
				audit_trail.add(value)

				flash(event.name.title() + ' was declined!', 'success')
				return redirect('/')

		else:

			flash('Invalid credentials! Please try again.', 'error')

	return render_template('/unregistered/events/signing.html', form=form, action=action, event=event)

