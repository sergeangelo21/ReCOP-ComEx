from flask import Blueprint, render_template
from blueprints.linkages.forms import ProposalForm
from data_access.models import event_information
import os

linkages = Blueprint('linkages', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@linkages.route('/linkages')
def index():

	return render_template('/linkages/index.html')

@linkages.route('/linkages/events')
def events():

	return render_template('/linkages/events.html')

@linkages.route('/linkages/proposals', methods=['GET', 'POST'])
def proposals():

	form = ProposalForm()

	if form.validate_on_submit():
		value = [1,1,1,form.title.data,form.purpose.data,form.venue.data,form.date.data,"A","A"]
		event_information.add(value)

	return render_template('/linkages/proposals.html', title="Proposals | Partners", form=form)

@linkages.route('/linkages/beneficiaries')
def beneficiaries():

	return render_template('/linkages/beneficiaries.html')

@linkages.route('/linkages/reports')
def reports():

	return render_template('/linkages/reports.html')

@linkages.route('/linkages/termsandconditions')
def termsandconditions():

	return render_template('/linkages/termsandconditions.html')

@linkages.route('/linkages/profile')
def profile():

	return render_template('/linkages/profile.html')