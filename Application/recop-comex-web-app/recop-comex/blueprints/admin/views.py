from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from flask_mail import Message
from blueprints.admin.forms import SearchForm
from data_access.models import *
from data_access.queries import *

from extensions import db, mail
from static.token import generate

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

@admin.route('/admin/events/filter_<status>_<search>', methods=['GET', 'POST'])
@login_required
def events(status, search):

	events = event_views.show_all()

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('admin.events', status=status, search=form.search.data))

	return render_template('/admin/events/index.html', title="Events | Admin", form=form, events=events, search=search)

@admin.route('/admin/events/show/id=<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)

	return render_template('/admin/events/show.html', title="Events | Admin", event = event)

@admin.route('/admin/events/create')
@login_required
def events_create():



	return render_template('/admin/events/create.html', )


@admin.route('/admin/partners/filter_<status>_<search>', methods=['GET', 'POST'])
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

	if user.status == "A":
		status = "D"
		flash("Partner was disabled!")
	else:

		if user.status=='N':
			
			token = generate(user.id)
			link = url_for('unregistered.confirm_partner', token=token , _external = True)
			html = render_template('email/moa.html', user = user.username, link = link)

			msg = Message(html=html,
				subject="Memorandum of Agreement for Partners",
				sender = ("ReCOP Community Extension", "recop.baste@gmail.com"),
				recipients=[user.email_address])

			mail.send(msg)
			
			new = 'MOA was sent to email.'
			status = "P"
			
			audit_id = audit_trail.count()
			value = [audit_id,id,'partner', 1]
			audit_trail.add(value)

		else:
			new = ''
			status = "A"

		flash("Partner was activated! " + new)

	user_account.update_status(id, status)

	return redirect(url_for('admin.partners', status='all', search=' '))

@admin.route('/admin/partners/create')
@login_required
def partners_create():



	return render_template('/admin/partners/create.html', )

@admin.route('/admin/beneficiaries')
@login_required
def beneficiaries():

	return render_template('/admin/beneficiaries.html', title="Beneficiaries | Admin")

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
