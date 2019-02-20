from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required
from blueprints.linkages.forms import *
from data_access.models import user_account, event_information, event_participation, proposal_tracker, user_information, event_attachment
from data_access.queries import user_views, linkage_views, event_views
from extensions import db, bcrypt
from static.pdf import generate_pdf
from datetime import datetime

import os

linkages = Blueprint('linkages', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@linkages.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))

		user_account.logout()

@linkages.route('/linkages/index')
@login_required
def index():

	return render_template('/linkages/index.html')

@linkages.route('/linkages/events')
@login_required
def events():

	events = event_views.show_list('all', ' ')

	return render_template('/linkages/events/index.html', events=events)

@linkages.route('/linkages/events/create', methods=['GET','POST'])
@login_required
def events_create():

	form = ProposalForm()

	linkages = linkage_views.target_linkages()

	for item in linkages:

		if item.type==3:
			name = item.company_name
		else:
			name = item.address

		form.select_link.choices.append((item.id, name))

	if form.validate_on_submit():

		det = user_information.linkage_info(current_user.info_id)

		if det.company_name=='San Sebastian College Recoletos de Cavite':
			event_type=1
		else:
			event_type=2

		value = [
		None,current_user.info_id,form.title.data,
		form.description.data,form.objective.data,form.budget.data,form.location.data,
		form.event_date.data,form.participant_no.data, form.min_age.data, form.max_age.data,
		form.thrust.data,event_type,'N'
		]

		
		event_information.add(value)

		event = event_information.last_added(current_user.id)

		if form.target_link.data:

			comm = form.target_link.data.split('|',-1)

			for participant in comm:

				if participant!='':
					value = [None, event.id, participant, 'Y']
					event_participation.add(value)

		budget_plan = form.budget_plan.data
		old, extension = os.path.splitext(budget_plan.filename)
		filename = str(event.id)+extension
		file_path = 'static/attachment/budget_plan/' + filename

		value = [None,event.id,file_path,1]

		event_attachment.add(value)
		budget_plan.save(file_path)

		programme = form.programme.data
		old, extension = os.path.splitext(programme.filename)
		filename = str(event.id)+extension
		file_path = 'static/attachment/programme/' + filename

		value = [None,event.id,file_path,2]

		event_attachment.add(value)
		programme.save(file_path)

		value = [None, event.id]
		proposal_tracker.add(value)

		flash('Event proposal submitted! Please download the request letter.', 'success')

		return redirect(url_for('linkages.events'))

	return render_template('/linkages/events/create.html', form=form)

@linkages.route('/linkages/events/letter/<id>_<name>', methods=['GET', 'POST'])
@login_required
def event_letter(id,name):

	filepath = 'static/output/events/letters/'

	event = event_views.show_info(id)

	html = render_template('linkages/pdf/pdf.html', event = event, date = datetime.now())

	generate_pdf(html, filepath + str(id) + '.pdf')

	return send_from_directory(filepath, str(id) +'.pdf')

@linkages.route('/linkages/communities')
@login_required
def communities():

	return render_template('/linkages/communities/index.html')

@linkages.route('/linkages/communities/referral')
@login_required
def referral():

	form = ReferralForm()

	return render_template('/linkages/communities/referral.html', form=form)

@linkages.route('/linkages/donate')
@login_required
def donate():

	form = DonationForm()

	linkages = linkage_views.target_linkages()

	for c in linkages:

		if c.type==4:
			form.sponsee.choices.extend([(str(c.id), c.address)])

	events = event_views.show_list('S', ' ')

	if events:
		form.event.choices.extend(([str(e.id), e.name] for e in events))
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

			is_event = 'N'
		else:
			sponsee = form.event.data
			is_event = 'Y'

		file = form.trans_slip.data
		old, extension = os.path.splitext(file.name)

		new = donation.last_added()
		filename = str(new)+extension

		trans_path = 'static/output/donate' + filename

		value = [None,sponsee,current_user.info_id,form.amount.data,trans_path,is_event]

		donation.add(value)
		file.save(trans_path)

		flash('Donation given!', 'success')
		return redirect(url_for('linkages.donate'))

	return render_template('/linkages/donate/index.html', form=form)

@linkages.route('/linkages/reports')
@login_required
def reports():

	return render_template('/linkages/reports/index.html')

@linkages.route('/linkages/contactus')
@login_required
def contactus():

	return render_template('/linkages/contactus/index.html')

@linkages.route('/linkages/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/linkages/termsandconditions/index.html')

@linkages.route('/linkages/profile/about/<user>')
@login_required
def profile_about(user):

	linkages = user_views.profile_info(current_user.info_id)

	return render_template('/linkages/profile/about.html', title="Linkages", linkages=linkages)

@linkages.route('/linkages/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/linkages/profile/eventsattended.html', title="Linkages")	

@linkages.route('/linkages/profile/settings/personal', methods=['GET', 'POST'])
@login_required
def profile_settings_personal():

	user_information_update = user_information.profile_info_update(current_user.info_id)

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

		return redirect(url_for('linkages.profile_settings_personal'))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/linkages/profile/settings/personal.html', title="Linkages", form=form)

@linkages.route('/linkages/profile/settings/contact', methods=['GET', 'POST'])
@login_required
def profile_settings_contact():

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

		return redirect(url_for('linkages.profile_settings_contact'))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/linkages/profile/settings/contact.html', title="Linkages", form=form)	

@linkages.route('/linkages/profile/settings/username', methods=['GET', 'POST'])
@login_required
def profile_settings_username():

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('linkages.profile_settings_username'))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/linkages/profile/settings/username.html', title="Linkages", form=form)

@linkages.route('/linkages/profile/update/password', methods=['GET', 'POST'])
@login_required
def profile_settings_password():

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('linkages.profile_settings_password'))

		else:

			flash('Wrong password.', 'error')

	return render_template('/linkages/profile/settings/password.html', title="Linkages", form=form)