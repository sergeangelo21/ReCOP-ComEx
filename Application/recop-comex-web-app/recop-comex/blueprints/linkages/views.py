from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory
from flask_login import current_user, login_required
from blueprints.linkages.forms import *
from data_access.models import user_account, event_information, event_participation, proposal_tracker, user_information, event_attachment, donation, referral
from data_access.queries import user_views, linkage_views, event_views
from extensions import db, bcrypt
from static.email import send_email
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

@linkages.route('/linkages/events/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def events(status, search):

	if status=='scheduled':
		value='S'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='declined':
		value='X'
	elif status=='finished':
		value='F'
	else:
		value=status

	events = event_views.show_list(value, search)

	letters = event_attachment.letter_attached()

	form = SearchForm()


	if form.validate_on_submit():



		return redirect(url_for('linkages.events', status=status, search=form.search.data))

	return render_template('/linkages/events/index.html', title="Events | linkages", form=form, events=events, status=status,letters=letters,search=search)

@linkages.route('/linkages/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	events = event_views.show_list('S', ' ')
	
	return render_template('/linkages/events/index-calendar.html', title="Events | linkages", events=events)
	
@linkages.route('/linkages/events/show/id=<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)
	participants = event_views.show_participants(id)

	return render_template('/linkages/events/show.html', title= event.name.title() + " | linkages", event = event, participants=participants)

@linkages.route('/linkages/events/create', methods=['GET', 'POST'])
@login_required
def events_create():

	form = ProposalForm()

	linkages = linkage_views.target_linkages()

	for item in linkages:

		if item.type==3:
			name = item.company_name
		else:
			name = item.address

		form.select_link.choices.extend([(item.id, name)])

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
		form.thrust.data,event_type,'P'
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

		signatory = user_views.signatory_info(4)

		recipient = signatory.email_address
		user = 'Fr. ' + signatory.last_name + ', OAR'
		token = generate(event.id)
		organizer='Recoletos Community Outreach Program Office'
		approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
		decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
		html = render_template('linkages/email/event.html', event=event , organizer=organizer, user=user, link = [approve, decline])
		attachments = event_attachment.retrieve_files(event.id)
		subject = "NEW EVENT PROPOSAL: " + event.name

		email_parts = [html, subject, current_user.email_address, recipient, attachments]

		send_email(email_parts)

		value = [None, event.id, 'A']
		proposal_tracker.add(value)

		flash('Event proposal submitted! Please wait for the approval.', 'success')

		return redirect(url_for('linkages.events', status='all', search=' '))


	return render_template('/linkages/events/create.html', form=form)

@linkages.route('/linkages/events/<action>/id=<id>')
@login_required
def event_action(id, action):

	event = event_information.retrieve_event(id)
	organizer = user_information.linkage_info(event.organizer_id)
	email = user_account.retrieve_user(organizer.id)

	if action=='approve':

		signatory = user_views.signatory_info(4)
		status = ['P','A']

		recipient = signatory.email_address
		user = 'Fr. ' + signatory.last_name + ', OAR'
		token = generate(event.id)
		approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
		decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
		html = render_template('linkages/email/event.html', event=event , organizer=organizer.company_name, user=user, link = [approve, decline])
		attachments = event_attachment.retrieve_files(id)
		subject = "NEW EVENT PROPOSAL: " + event.name

		email_parts = [html, subject, current_user.email_address, recipient, attachments]

		send_email(email_parts)

		event_information.update_status(event.id,status[0])
		proposal_tracker.update_status(event.id,status[1])

		proposal = proposal_tracker.query.filter(proposal_tracker.event_id==event.id).first()

		value = [None,current_user.id,event.id,'event', 5]
		audit_trail.add(value)

		flash(event.name + ' was approved!', 'success')

	elif action=='decline':

		status='X'
		proposal_tracker.update_status(event.id, status)
		event_information.update_status(event.id, status)

		value = [None,current_user.id,event.id,'event', 6]
		audit_trail.add(value)

		flash(event.name + ' was declined.', 'info') 	


	return redirect(url_for('linkages.events', status='all', search=' '))

@linkages.route('/linkages/communities')
@login_required
def communities():

	return render_template('/linkages/communities/index.html')

@linkages.route('/linkages/donate', methods=['GET', 'POST'])
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

			event = None
		else:
			event = form.event.data
			sponsee= None

		file = form.trans_slip.data
		old, extension = os.path.splitext(file.name)

		new = donation.last_added()
		filename = str(new)+extension

		trans_path = 'static/output/donate' + filename

		value = [None,sponsee,event,current_user.info_id,form.amount.data,trans_path,'N']

		donation.add(value)
		file.save(trans_path)

		flash('Donation given!', 'success')
		return redirect(url_for('linkages.donate'))

	return render_template('/linkages/donate/index.html', form=form, no_event=no_event)

@linkages.route('/linkages/reports')
@login_required
def reports():

	return render_template('/linkages/reports/index.html')

@linkages.route('/linkages/referral', methods=['GET', 'POST'])
@login_required
def referral_users():

	form = ReferralForm()

	if form.validate_on_submit():

		html = 'asdlkfjasfd'
		subject = 'REFFERAL: '
		admin = user_account.query.filter_by(id=1).first()

		email_parts = [html, subject, admin.email_address, form.email.data, None]
		send_email(email_parts)

		value = [None, current_user.id, form.name.data, form.email.data, form.type.data, 'N']

		referral.add(value)

		flash('Referral has been sent!', 'success')
		return redirect(url_for('linkages.referral_users'))	

	return render_template('/linkages/referral/index.html', form=form)

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