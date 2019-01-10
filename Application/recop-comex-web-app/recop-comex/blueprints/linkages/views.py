from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from blueprints.linkages.forms import ProposalForm
from data_access.models import event_information, event_category, proposal_tracker
import os

linkages = Blueprint('linkages', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

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
		value = [id,1,form.category.data,form.title.data,'event ko to', form.purpose.data,1000.50,form.venue.data,form.date.data,1,'N']
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