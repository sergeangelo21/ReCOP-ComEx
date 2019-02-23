from flask import Blueprint, render_template, url_for, redirect, flash, send_from_directory
from flask_login import current_user, login_required
from blueprints.admin.forms import *
from data_access.models import *
from data_access.queries import *
from static.email import generate, send_email
from sqlalchemy import or_
import os, pygal

admin = Blueprint('admin', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@admin.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:
		if current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))

		user_account.logout()

@admin.route('/admin')
@login_required
def index():

	events_chart = pygal.Bar()
	events_chart.title = 'Events'

	events_chart.add('Education', [100])
	events_chart.add('Environmental', [100])
	events_chart.add('Health', [100])
	events_chart.add('Livelihood', [100])
	events_chart.add('Socio-political', [100])
	events_chart.add('Spiritual', [100])

	events_chart.render_response()

	return render_template('/admin/index.html', title="Home | Admin", events_chart=events_chart)

@admin.route('/admin/events/<status>/filter_<search>', methods=['GET', 'POST'])
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

		return redirect(url_for('admin.events', status=status, search=form.search.data))

	return render_template('/admin/events/index.html', title="Events | Admin", form=form, events=events, status=status,letters=letters,search=search)

@admin.route('/admin/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	events = event_views.show_list('S', ' ')
	
	return render_template('/admin/events/index-calendar.html', title="Events | Admin", events=events)
	
@admin.route('/admin/events/show/id=<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)
	participants = event_views.show_participants(id)

	return render_template('/admin/events/show.html', title= event.name.title() + " | Admin", event = event, participants=participants)

@admin.route('/admin/events/create')
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

		return redirect(url_for('admin.events'))


	return render_template('/admin/events/create.html', form=form)

@admin.route('/admin/events/<action>/id=<id>')
@login_required
def event_action(id, action):

	event = event_information.retrieve_event(id)
	organizer = user_information.linkage_info(event.organizer_id)
	email = user_account.retrieve_user(organizer.id)

	if action=='approve':

		signatory = user_views.signatory_info(4)
		status = ['P','A']

		recipient = signatory.email_address
		user = 'Fr. ' + signatory.last_name
		token = generate(event.id)
		approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
		decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
		html = render_template('admin/email/event.html', event=event , organizer=organizer.company_name, user=user, link = [approve, decline])
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


	return redirect(url_for('admin.events', status='all', search=' '))


@admin.route('/admin/linkages/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def linkages(status, search):

	if status=='active':
		value='A'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='disabled':
		value='D'
	else:
		value=status

	linkages = linkage_views.show_list(value, 3, search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.linkages', status=status, search=form.search.data))

	return render_template('/admin/linkages/index.html', title="Linkages | Admin", form=form, linkages=linkages, status=status, search=search)

@admin.route('/admin/linkages/create')
@login_required
def linkages_create():

	return render_template('/admin/linkages/create.html')

@admin.route('/admin/linkages/show/id=<id>')
@login_required
def linkage_show(id):

	linkage, mem_since = linkage_views.show_info([id,'linkage'])

	return render_template('/admin/linkages/show.html', title= linkage.company_name.title() + " | Admin", linkage=linkage, mem_since=mem_since)

@admin.route('/admin/linkages/action/id=<id>')
@login_required
def linkage_action(id):

	user = user_account.retrieve_user(id)
	linkage = user_information.linkage_info(user.info_id)

	if user.status == "A":
	
		status = "D"
		flash(linkage.company_name.title() + " was disabled!","success")

		value = [None,current_user.id,user.id,'linkage', 4]
		audit_trail.add(value)
	
	elif user.status== "D":
		
		status = "A"
		flash(linkage.company_name.title() + " was activated! ", "success")

		value = [None,current_user.id,user.id,'linkage', 3]
		audit_trail.add(value)

	else:

		if linkage.address == "San Sebastian College Recoletos de Cavite":

			status = "A"
			flash(linkage.company_name.title() + " was activated! ", "success")
			value =	 [None,current_user.id,user.id,'linkage', 2]
			audit_trail.add(value)	

		else:

			token = generate(user.info_id)
			link = url_for('unregistered.confirm_linkage', token=token , _external = True)	
			html = render_template('admin/email/moa.html', user = user.username+', OAR', link = link)
			subject = "MEMORANDUM OF AGREEMENT"

			email_parts = [html, subject, current_user.email_address, user.email_address, None]

			send_email(email_parts)
			
			flash('MOA was sent to ' + linkage.company_name.title(), 'success')

			status = "P"
			
			value = [None,current_user.id,user.id,'linkage', 1]
			audit_trail.add(value)

	user_account.update_status(user.id, status)

	return redirect(url_for('admin.linkages', status='all', search=' '))

@admin.route('/admin/communities/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def communities(status, search):

	if status=='active':
		value='A'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='disabled':
		value='D'
	else:
		value=status

	communities = linkage_views.show_list(value, 4, search=search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.communities', status=status, search=form.search.data))

	return render_template('/admin/communities/index.html', title="Communities | Admin", form=form, communities=communities, status=status, search=search)

@admin.route('/admin/communities/create')
@login_required
def communities_create():

	return render_template('/admin/communities/create.html')

@admin.route('/admin/communities/show/id=<id>')
@login_required
def community_show(id):

	community, mem_since = linkage_views.show_info([id,'community'])

	return render_template('/admin/communities/show.html', title= community.company_name.title() + " | Admin", community=community, mem_since=mem_since)

@admin.route('/admin/communities/action/id=<id>')
@login_required
def community_action(id):

	user = user_account.retrieve_user(id)
	community = user_information.linkage_info(user.info_id)

	if user.status == "A":
	
		status = "D"
		flash(community.company_name.title() + " was disabled!","success")

		value = [None,current_user.id,user.id,'community', 4]
		audit_trail.add(value)
	
	elif user.status== "D":
		
		status = "A"
		flash(community.company_name.title() + " was activated! ", "success")

		value = [None,current_user.id,user.id,'community', 3]
		audit_trail.add(value)

	else:
			
		token = generate(user.info_id)
		link = url_for('unregistered.confirm_linkage', token=token , _external = True)	
		html = render_template('admin/email/moa.html', user = user.username, link = link)
		subject = "MEMORANDUM OF AGREEMENT"

		email_parts = [html, subject, current_user.email_address, user.email_address, None]

		send_email(email_parts)
			
		flash('MOA was sent to ' + community.company_name.title(), 'success')

		status = "P"
			
		value = [None,current_user.id,user.id,'community', 1]
		audit_trail.add(value)

	user_account.update_status(user.id, status)

	return redirect(url_for('admin.communities', status='all', search=' '))

@admin.route('/admin/donations/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def donations(status, search):	

	if status=='new':
		value='N'
	elif status=='received':
		value='R'
	elif status=='declined':
		value='D'
	else:
		value=status

	donations=donation_views.show_list(value, search)

	sponsors = donation_views.show_sponsors()

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.donations', status=status, search=form.search.data))	

	return render_template('/admin/donations/index.html', title="Donations | Admin", donations=donations, sponsors=sponsors, status=status, search=search, form=form)

@admin.route('/admin/donations/<action>/id=<id>')
@login_required
def donation_action(id,action):

	if action=='trans_slip':
		
		info = donation.retrieve_donation(id)
		filepath = info.transaction_slip
		name = filepath.rsplit('/',1)[1]
		path = filepath.rsplit('/',1)[0]
		return send_from_directory(path, name, title='asd')	

	elif action=='receive':

		info = donation.retrieve_donation(id)

		if info.amount==0.00:

			return redirect(url_for('admin.donation_inkind', id=id))

		else:
			donation.update_status([id,'R'])
			flash('Donation was received', 'success')

		return redirect(url_for('admin.donations', status='all', search=' '))

	else:
		donation.update_status([id,'D'])
		flash('Donation was declined.', 'success')
		return redirect(url_for('admin.donations', status='all', search=' '))

@admin.route('/admin/donations/inkind/<id>', methods=['GET', 'POST'])
@login_required
def donation_inkind(id):	

	info = donation.retrieve_donation(id)

	types = inventory_type.show_list()

	form = AddInventoryForm()

	form.type.choices.extend([(t.id, t.name) for t in types])

	if form.validate_on_submit():

		return form.types.data

	return render_template('/admin/donations/add.html', title="Donation | Admin", form=form, donation=info)

@admin.route('/admin/inventory/filter_<search>')
@login_required
def inventory(search):

	form = SearchForm()

	types = inventory_type.show_list()

	if form.validate_on_submit():

		return redirect(url_for('admin.communities', search=form.search.data))

	return render_template('/admin/inventory/index.html', title="Inventory | Admin", form=form, types=types, search=search)

@admin.route('/admin/inventory/add')
@login_required
def inventory_add():

	return render_template('/admin/inventory/add.html', title="Inventory | Admin")

@admin.route('/admin/inventory/add_type', methods=['GET', 'POST'])
@login_required
def inventory_add_type():

	form = AddTypeInventoryForm()

	if form.validate_on_submit():

		value = [None, form.name.data, 'A']

		inventory_type.add(value)
		id = inventory_type.last_added()

		value = [None,current_user.id,id,'inventory', 1]
		audit_trail.add(value)

		flash('Inventory type added!', 'success')
		return redirect(url_for('admin.inventory', search=' '))

	return render_template('/admin/inventory/add_type.html', title="Inventory | Admin", form=form)

@admin.route('/admin/feedbacks')
@login_required
def feedbacks():

	return render_template('/admin/feedbacks/index.html', title="Feedbacks | Admin")

@admin.route('/admin/referral')
@login_required
def referral():

	return render_template('/admin/referral/index.html', title="referral | Admin")

@admin.route('/admin/profile/about/<user>')
@login_required
def profile_about(user):

	admin = user_views.profile_info(current_user.info_id)

	return render_template('/admin/profile/about.html', title="Admin", admin=admin)

@admin.route('/admin/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/admin/profile/eventsattended.html', title="Admin")	

@admin.route('/admin/profile/settings/personal_<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_personal(user):

	if user == 'academicservices':
		value = 4
	elif user == 'formationmissionidentity':
		value = 3
	elif user == 'president':
		value = 2
	else:
		value = 1

	user_information_update = user_information.profile_info_update(value)

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

		return redirect(url_for('admin.profile_settings_personal', user=user))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/admin/profile/settings/personal.html', title="Admin", form=form)

@admin.route('/admin/profile/settings/contact_<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_contact(user):

	if user == 'academicservices':
		value = 4
	elif user == 'formationmissionidentity':
		value = 3
	elif user == 'president':
		value = 2
	else:
		value = 1

	user_information_update = user_information.profile_info_update(value)
	user_account_update = user_account.profile_acc_update(value)

	form = ProfileContactUpdateForm()

	if form.validate_on_submit():

		user_information_update.address = form.address.data
		user_information_update.telephone = form.telephone.data
		user_information_update.mobile_number = form.mobile.data

		db.session.commit()

		user_account_update.email_address = form.email.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('admin.profile_settings_contact', user=user))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/admin/profile/settings/contact.html', title="Admin", form=form)	

@admin.route('/admin/profile/settings/username_<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_username(user):

	if user == 'academicservices':
		value = 4
	elif user == 'formationmissionidentity':
		value = 3
	elif user == 'president':
		value = 2
	else:
		value = 1

	user_account_update = user_account.profile_acc_update(value)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user_val = user_account.login([current_user.username, form.oldpassword.data])

		if user_val:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('admin.profile_settings_username', user=user))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/admin/profile/settings/username.html', title="Admin", form=form)

@admin.route('/admin/profile/update/password_<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_password(user):

	if user == 'academicservices':
		value = 4
	elif user == 'formationmissionidentity':
		value = 3
	elif user == 'president':
		value = 2
	else:
		value = 1

	user_account_update = user_account.profile_acc_update(value)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user_val = user_account.login([current_user.username, form.oldpassword.data])

		if user_val:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('admin.profile_settings_password', user=user))

		else:

			flash('Wrong password.', 'error')

	return render_template('/admin/profile/settings/password.html', form=form)