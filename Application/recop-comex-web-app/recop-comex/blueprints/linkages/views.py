from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from blueprints.linkages.forms import ProposalForm
from data_access.models import user_account, event_information, proposal_tracker, user_information

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
			return redirect(url_for('beneficiaries.index'))

@linkages.route('/linkages')
@login_required
def index():

	return render_template('/linkages/index.html')

@linkages.route('/linkages/events')
@login_required
def events():

	events = event_information.query.all()

	return render_template('/linkages/events/index.html', events=events)

@linkages.route('/linkages/events/create', methods=['GET','POST'])
@login_required
def events_create():

	form = ProposalForm()

	if form.validate_on_submit():

		det = user_information.query.filter(user_information.id==current_user.info_id).first()

		if det.company_name=='San Sebastian College Recoletos de Cavite':
			event_type=1
		else:
			event_type=2

		id = event_information.count()
		value_event = [
		id,current_user.info_id,form.title.data,
		form.description.data,form.objective.data,form.budget.data,form.location.data,
		form.event_date.data,form.thrust.data,event_type,'N'
		]

		event_information.add(value_event)

		id = proposal_tracker.count()
		value_tracker = [id, value_event[0]]
		proposal_tracker.add(value_tracker)

		flash('Event proposal submitted! Please standby for the approval.')

		return redirect(url_for('linkages.events'))

	return render_template('/linkages/events/create.html', form=form)

@linkages.route('/linkages/beneficiaries')
@login_required
def beneficiaries():

	return render_template('/linkages/beneficiaries.html')

@linkages.route('/linkages/reports')
@login_required
def reports():

	return render_template('/linkages/reports.html')

@linkages.route('/linkages/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/linkages/termsandconditions.html')

@linkages.route('/linkages/profile/about')
@login_required
def profile_about():

	return render_template('/linkages/profile/about.html')	

@linkages.route('/linkages/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/linkages/profile/eventsattended.html')	

@linkages.route('/linkages/profile/settings')
@login_required
def profile_settings():

	return render_template('/linkages/profile/settings.html')	


