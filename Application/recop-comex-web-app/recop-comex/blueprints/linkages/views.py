from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from blueprints.linkages.forms import ProposalForm
from data_access.models import user_account, event_information, event_category, proposal_tracker, user_information
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

	return render_template('/linkages/events.html')

@linkages.route('/linkages/proposals', methods=['GET', 'POST'])
@login_required
def proposals():

	form = ProposalForm()

	form.category.choices = event_category.select()

	if form.validate_on_submit():
		id = event_information.count()
		value = [
		id,1,form.category.data,form.title.data,
		form.description.data,form.objective.data,form.budget.data,form.location.data,
		form.event_date.data,1,'N'
		]
		event_information.add(value)
		return redirect(url_for('linkages.proposals'))

	return render_template('/linkages/proposals.html', title="Proposals | Partners", form=form)

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

@linkages.route('/linkages/profile')
@login_required
def profile():

	return render_template('/linkages/profile.html')