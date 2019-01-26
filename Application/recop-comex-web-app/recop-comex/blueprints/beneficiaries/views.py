from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required
from blueprints.beneficiaries.forms import ProposalForm
from data_access.models import user_account, user_information,proposal_tracker

import os

beneficiaries = Blueprint('beneficiaries', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@beneficiaries.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))

@beneficiaries.route('/beneficiaries')
@login_required
def index():

	return render_template('/beneficiaries/index.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/events')
@login_required
def events():

	return render_template('/beneficiaries/events/_events.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/events/create')
@login_required
def create():

	form = ProposalForm()

	if form.validate_on_submit():

		id = event_information.count()
		value_event = [
		id,current_user.id,form.category.data,form.title.data,
		form.description.data,form.objective.data,form.budget.data,form.location.data,
		form.event_date.data,1,'N'
		]

		event_information.add(value_event)

		id = proposal_tracker.count()
		value_tracker = [id, value_event[0]]
		proposal_tracker.add(value_tracker)

		event_information.add(value)
		return redirect(url_for('beneficiaries.events'))



	return render_template('/beneficiaries/events/create.html', title="Beneficiaries", form=form)

@beneficiaries.route('/beneficiaries/reports')
@login_required
def reports():

	return render_template('/beneficiaries/reports.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/contactus')
@login_required
def contactus():

	return render_template('/beneficiaries/contactus.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/beneficiaries/termsandconditions.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/profile')
@login_required
def profile():

	return render_template('/beneficiaries/profile.html', title="Beneficiaries")
