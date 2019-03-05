from flask import Blueprint, render_template, url_for, redirect, flash, send_from_directory, request
from flask_login import current_user, login_required
from blueprints.admin.forms import *
from data_access.models import *
from data_access.queries import *
from static.email import generate, send_email
from sqlalchemy import or_
import os, pygal

from extensions import db

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

	return render_template('/admin/index.html', title="Home | Admin", events_chart=events_chart, active='home')

@admin.route('/admin/events/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def events(status, page, search):

	if status=='scheduled':
		value='S'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='declined':
		value='X'
	elif status=='cancelled':
		value='C'
	elif status=='finished':
		value='F'
	else:
		value=status

	events = event_views.show_list([value, search, page])

	letters = event_attachment.letter_attached()

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.events', status=status, page='1', search=form.search.data))

	return render_template('/admin/events/index.html', title="Events | Admin", form=form, events=events, status=status, letters=letters, search=search, active='events')

@admin.route('/admin/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	events = event_views.select_list()
	
	return render_template('/admin/events/index-calendar.html', title="Events | Admin", events=events, active='events')
	
@admin.route('/admin/events/show/id=<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)
	participants = event_views.show_participants(id)

	return render_template('/admin/events/show.html', title= event.name.title() + " | Admin", event = event, participants=participants, active='events')

@admin.route('/admin/events/create', methods=['GET', 'POST'])
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

		signatory = user_views.signatory_info(3)

		recipient = signatory.email_address
		user = 'Fr. ' + signatory.last_name + ', OAR'
		token = generate(event.id)
		organizer='Recoletos Community Outreach Program Office'
		approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
		decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
		html = render_template('admin/email/event.html', event=event , organizer=organizer, user=user, link = [approve, decline])
		attachments = event_attachment.retrieve_files(event.id)
		subject = "NEW EVENT PROPOSAL: " + event.name

		email_parts = [html, subject, current_user.email_address, recipient, attachments]

		send_email(email_parts)

		value = [None, event.id, 'F']
		proposal_tracker.add(value)
		proposal_tracker.update_status(event.id, 'F')

		flash('Event proposal submitted! Please wait for the approval.', 'success')

		return redirect(url_for('admin.events', status='all', page='1', search=' '))

	return render_template('/admin/events/create.html', title="Create Event | Admin", form=form, active='events')

@admin.route('/admin/events/reschedule/id=<id>', methods=['GET', 'POST'])
@login_required
def event_reschedule(id):

	form = RescheduleEventForm()

	resched_event = event_information.reschedule(current_user.id)

	if form.validate_on_submit():

		resched_event.location = form.location.data
		resched_event.event_date = form.event_date.data

		db.session.commit()

		flash('Event rescheduled!', 'success')

		return redirect(url_for('admin.events', status='all', page='1', search=' '))

	else:

		form.location.data = resched_event.location
		form.event_date.data = resched_event.event_date

	return render_template('/admin/events/reschedule.html', title="Reschedule | Admin", form=form, event=resched_event, active='events')

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
		user = 'Fr. ' + signatory.last_name + ', OAR'
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

	elif action=='cancel':

		status='C'
		proposal_tracker.update_status(event.id, status)
		event_information.update_status(event.id, status)

		value = [None,current_user.id,event.id,'event', 8]
		audit_trail.add(value)

		flash(event.name + ' was cancelled.', 'success')	


	return redirect(url_for('admin.events', status='all', page='1', search=' '))

@admin.route('/admin/linkages/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def linkages(status, page, search):

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

	linkages = linkage_views.show_list([value,search,3,page])

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.linkages', status=status, page='1', search=form.search.data))

	return render_template('/admin/linkages/index.html', title="Linkages | Admin", form=form, linkages=linkages, status=status, search=search, active='linkages')

@admin.route('/admin/linkages/chart')
@login_required
def linkages_chart():

	query = db.session.query(user_account, func.count(user_account.type)).filter(user_account.type==3).all()

	flash(query)

	chart = pygal.Pie()
	chart.title = 'Linkages'

	for type in query:
		chart.add('asd', [])

	chart.render_response()

	return render_template('/admin/linkages/chart.html', title="Linkages | Admin", chart=chart, active='linkages')

@admin.route('/admin/linkages/add', methods=['GET', 'POST'])
@login_required
def linkages_add():

	form = AddLinkageForm()

	if form.validate_on_submit():

		value = [
			None,form.firstname.data,form.middlename.data,
			form.lastname.data,form.company.data,form.bio.data,form.gender.data,form.birthday.data,
			form.address.data,form.telephone.data,form.mobile.data,form.thrust.data
			]

		user_information.add(value)	
		user_id = user_information.reserve_id()

		status = "N"

		value = [
			None,user_id,form.username.data,
			form.password.data,form.email.data,3,datetime.now(),status
			]

		user_account.add(value)

		flash('Linkage '+form.company.data+' was successfully added!', 'success')

		return redirect(url_for('admin.linkages', status='all', page='1', search=' '))	

	return render_template('/admin/linkages/add.html', title="Add Linkage | Admin", form=form, active='linkages')

@admin.route('/admin/linkages/show/id=<id>')
@login_required
def linkage_show(id):

	linkage, mem_since = linkage_views.show_info([id,'linkage'])

	return render_template('/admin/linkages/show.html', title= linkage.company_name.title() + " | Admin", linkage=linkage, mem_since=mem_since, active='linkages')

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

	return redirect(url_for('admin.linkages', status='all', page='1', search=' '))

@admin.route('/admin/communities/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def communities(status, page, search):

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

	communities = linkage_views.show_list([value,search,4,page])

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.communities', status=status, page='1', search=form.search.data))

	return render_template('/admin/communities/index.html', title="Communities | Admin", form=form, communities=communities, status=status, search=search, active='communities')

@admin.route('/admin/communities/chart')
@login_required
def communities_chart():

	chart = pygal.Pie()
	chart.title = 'Communities'

	chart.add('Education', [100])
	chart.add('Environmental', [100])
	chart.add('Health', [100])
	chart.add('Livelihood', [100])
	chart.add('Socio-political', [100])
	chart.add('Spiritual', [100])

	chart.render_response()

	return render_template('/admin/communities/chart.html', title="Communities | Admin", chart=chart, active='communities')

@admin.route('/admin/communities/add', methods=['GET', 'POST'])
@login_required
def communities_add():

	form = AddCommunityForm()

	if form.validate_on_submit():

		value = [
			None,form.firstname.data,form.middlename.data,form.lastname.data,
			'San Sebastian College Recoletos de Cavite',form.bio.data,form.gender.data,form.birthday.data,
			form.address.data,form.telephone.data,form.mobile.data,0
			]

		user_information.add(value)	
		user_id = user_information.reserve_id()

		status = "N"

		value = [
			None,user_id,form.username.data,
			form.password.data,form.email.data,4,datetime.now(),status
			]

		user_account.add(value)

		flash('Community was successfully added!', 'success')

		return redirect(url_for('admin.communities', status='all', page='1', search=' '))

	return render_template('/admin/communities/add.html', title="Add Community | Admin", form=form, active='communities')

@admin.route('/admin/communities/show/id=<id>')
@login_required
def community_show(id):

	community, mem_since = linkage_views.show_info([id,'community'])

	return render_template('/admin/communities/show.html', title= community.company_name.title() + " | Admin", community=community, mem_since=mem_since, active='communities')

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
			
		flash('MOA was sent to ' + community.address.title(), 'success')

		status = "P"
			
		value = [None,current_user.id,user.id,'community', 1]
		audit_trail.add(value)

	user_account.update_status(user.id, status)

	return redirect(url_for('admin.communities', status='all', search=' '))

@admin.route('/admin/donations/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def donations(status, page, search):	

	if status=='new':
		value='N'
	elif status=='received':
		value='R'
	elif status=='declined':
		value='D'
	else:
		value=status

	donations=donation_views.show_list([value, search,page])

	sponsors = donation_views.show_sponsors()

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.donations', status=status, page='1', search=form.search.data))	

	return render_template('/admin/donations/index.html', title="Donations | Admin", donations=donations, sponsors=sponsors, status=status, search=search, form=form, active='donations')

@admin.route('/admin/donations/<action>/id=<id>')
@login_required
def donation_action(id,action):

	if action=='trans_slip':
		
		info = donation.retrieve_donation(id)
		filepath = info.transaction_slip
		name = filepath.rsplit('/',1)[1]
		path = filepath.rsplit('/',1)[0]
		return send_from_directory(path, name)	

	elif action=='receive':

		info = donation.retrieve_donation(id)

		if info.amount==0.00:

			return redirect(url_for('admin.donation_inkind', id=id))

		else:
			donation.update_status([id,'R'])
			flash('Donation was received', 'success')

		return redirect(url_for('admin.donations', status='all', page='1', search=' '))

	else:
		donation.update_status([id,'D'])
		flash('Donation was declined.', 'success')
		return redirect(url_for('admin.donations', status='all', page='1', search=' '))

@admin.route('/admin/donations/inkind/<id>', methods=['GET', 'POST'])
@login_required
def donation_inkind(id):	

	info = donation.retrieve_donation(id)

	types = inventory_type.show_list()

	form = AddInventoryForm()

	form.type_select.choices.extend([(str(t.id), t.name) for t in types])

	if form.validate_on_submit():

		inv_type = form.types.data.split('|',-1)
		in_stock = form.quantities.data.split('|',-1)
		index=0

		for type in inv_type:

			if type!='':
				value=[None, info.id, type, in_stock[index], 0,0]
				inventory.add(value)
				index+=1

		donation.update_status([info.id,'R'])

		flash('Items were successfully added!', 'success')
		return redirect(url_for('admin.donations', status='all', page='1', search=' '))

	return render_template('/admin/donations/inventory.html', title="Donation | Admin", form=form, donation=info, active='donations')

@admin.route('/admin/donations/add', methods=['GET', 'POST'])
@login_required
def donation_add():	

	form=DonationForm()

	organizations = linkage_views.target_linkages()

	for o in organizations:

		if o.type==4:
			form.sponsee.choices.extend([(str(o.id), o.address)])
		else:
			form.sponsor.choices.extend([(str(o.id), o.company_name)])

	events = event_views.select_list()

	if events:
		for e in events:
			form.event.choices.extend([(str(e.id), e.name)])
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

		value = [None,sponsee,event,1,form.amount.data,trans_path,'N']

		donation.add(value)
		file.save(trans_path)

		flash('Donation given!', 'success')
		return redirect(url_for('admin.donations', status='all', page='1', search=' '))

	return render_template('/admin/donations/add.html', title="Donation | Admin", form=form, no_event=no_event, active='donations')

@admin.route('/admin/inventory/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def inventory_show(page, search):

	form = SearchForm()

	update = UpdateForm()

	items = inventory_views.show_list([search,page])

	breakdown = inventory.item_breakdown()

	if form.validate_on_submit():

		return redirect(url_for('admin.inventory_show', page='1', search=form.search.data))

	if update.validate_on_submit():

		print(update.submit)

	return render_template('/admin/inventory/index.html', title="Inventory | Admin", form=form, update=update, items=items, breakdown=breakdown, search=search, active='inventory')

@admin.route('/admin/inventory/add', methods=['GET', 'POST'])
@login_required
def inventory_add():

	form = NewInventoryForm()

	organizations = linkage_views.target_linkages()

	for o in organizations:

		if o.type==4:
			form.sponsee.choices.extend([(str(o.id), o.address)])
		else:
			form.sponsor.choices.extend([(str(o.id), o.company_name)])

	events = event_views.select_list()

	if events:
		for e in events:
			form.event.choices.extend([(str(e.id), e.name)])
			no_event = 0
			
	else: 
		form.event.data=''
		no_event = 1

	items = inventory_type.show_list()

	if items:
		for i in items:
			form.items.choices.extend([(str(i.id), i.name)])
			no_item = 0
			
	else: 
		form.items.data=''
		no_item = 1		

	if form.validate_on_submit():

		if form.is_donation.data=='1':
			
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

			donation_id = donation.last_added()
			filename = str(donation_id)+extension

			trans_path = 'static/output/donate/trans_slip/' + filename

			value = [None,sponsee,event,form.sponsor.data,0,trans_path,'R']

			donation.add(value)
			file.save(trans_path)

		else:
			donation_id=None

		if form.item_type.data=='1':
			value = [None, form.name.data, 'A']

			inventory_type.add(value)
			id = inventory_type.last_added()

			value = [None,current_user.id,id,'inventory', 1]
			audit_trail.add(value)

		else:

			id=form.items.data

		value=[None, donation_id, id, form.quantity.data , 0,0]
		inventory.add(value)

		flash('Inventory type added!', 'success')
		return redirect(url_for('admin.inventory_show', page='1', search=' '))

	return render_template('/admin/inventory/add.html', title="Inventory | Admin", form=form, no_event=no_event, no_item=no_item, active='inventory')

@admin.route('/admin/feedbacks')
@login_required
def feedbacks():

	return render_template('/admin/feedbacks/index.html', title="Feedbacks | Admin", active='feedbacks')

@admin.route('/admin/referral')
@login_required
def referral():

	return render_template('/admin/referral/index.html', title="Referral | Admin", active='referral')

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