from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_mail import Message
from blueprints.admin.forms import SearchForm
from data_access.models import *
from data_access.queries import *

from extensions import db, mail
from static.email import generate

import os

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
			return redirect(url_for('beneficiaries.index'))

@admin.route('/admin')
@login_required
def index():

	return render_template('/admin/index.html', title="Admin")

@admin.route('/admin/events/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def events(status, search):

	if status=='scheduled':
		value='S'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='finished':
		value='F'
	else:
		value=status

	events = event_views.show_list(value, search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.events', status=status, search=form.search.data))

	return render_template('/admin/events/index.html', title="Events | Admin", form=form, events=events, status=status,search=search)

@admin.route('/admin/events/show/id=<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)

	return render_template('/admin/events/show.html', title="Events | Admin", event = event)

@admin.route('/admin/events/create')
@login_required
def events_create():



	return render_template('/admin/events/create.html' )

@admin.route('/admin/events/<action>/id=<id>')
@login_required
def event_action(id, action):

	event = event_information.retrieve_event(id)
	organizer = user_information.partner_info(event.organizer_id)
	email = user_account.retrieve_user(organizer.id)

	if action=='approve':

		status = ['P','B']

		if event.budget>0.00:
			recipient = 'fmi.baste@gmail.com'
			user = 'Fr. Somebody'
		else:
			recipient = 'acad.baste@gmail.com'
			user = 'Fr. Tanquis'

		token = generate(event.id)
		approve = url_for('unregistered.event_signing', token=token , action='approve', _external = True)
		decline = url_for('unregistered.event_signing', token=token , action='decline', _external = True)		
		html = render_template('admin/email/event.html', event=event , organizer=organizer.company_name, user=user, link = [approve, decline])
		subject = "NEW EVENT: " + event.name

		email_parts = [html, subject, recipient]

		msg = compose_email(email_parts)

		mail.send(msg)

		flash(event.name + ' was approved!', 'success')

	elif action=='decline':

		status = 'X'

		flash(event.name + ' was declined.', 'info') 	


	return redirect(url_for('admin.events', status='all', search=' '))


@admin.route('/admin/partners/<status>/filter_<search>', methods=['GET', 'POST'])
@login_required
def partners(status, search):

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

	partners = partner_views.show_list(value, search=search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.partners', status=status, search=form.search.data))

	return render_template('/admin/partners/index.html', title="Partners | Admin", form=form, partners=partners, status=status, search=search)

@admin.route('/admin/partners/show/id=<id>')
@login_required
def partner_show(id):

	partner, mem_since = partner_views.show_info(id)

	return render_template('/admin/partners/show.html', title="Partners | Admin", partner=partner, mem_since = mem_since)

@admin.route('/admin/partners/action/id=<id>')
@login_required
def partner_action(id):

	user = user_account.retrieve_user(id)
	partner = user_information.partner_info(user.info_id)

	if user.status == "A":
	
		status = "D"
		flash(partner.company_name + " was disabled!","success")

		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,id,'partner', 4]
		audit_trail.add(value)
	
	elif user.status== "D":
		
		status = "A"
		flash(partner.company_name + " was activated! ", "success")

		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,id,'partner', 3]
		audit_trail.add(value)

	else:
			
		token = generate(user.id)
		link = url_for('unregistered.confirm_partner', token=token , _external = True)	
		html = render_template('admin/email/moa.html', user = user.username, link = link)
		subject = "MEMORANDUM OF AGREEMENT"

		email_parts = [html, subject, user.email_address]

		msg = compose_email(email_parts)

		mail.send(msg)
			
		flash('MOA was sent to ' + partner.company_name, 'success')

		status = "P"
			
		audit_id = audit_trail.count()
		value = [audit_id,current_user.id,id,'partner', 1]
		audit_trail.add(value)

	user_account.update_status(id, status)

	return redirect(url_for('admin.partners', status='all', search=' '))

@admin.route('/admin/partners/create')
@login_required
def partners_create():



	return render_template('/admin/partners/create.html')

@admin.route('/admin/beneficiaries')
@login_required
def beneficiaries():

	return render_template('/admin/beneficiaries.html', title="Beneficiaries | Admin")

@admin.route('/admin/donations')
@login_required
def donations():

	return render_template('/admin/donations.html', title="Donations | Admin")

@admin.route('/admin/reports')
@login_required
def reports():

	return render_template('/admin/reports.html', title="Reports | Admin")

@admin.route('/admin/feedbacks')
@login_required
def feedbacks():

	return render_template('/admin/feedbacks.html', title="Feedbacks | Admin")

@admin.route('/admin/profile')
@login_required
def profile():

	return render_template('/admin/profile.html', title="Profile | Admin")

def compose_email(parts):

	msg = Message(html=parts[0],
		subject=parts[1],
		sender = ("ReCOP Director", current_user.email_address),
		recipients=[parts[2]])

	return msg