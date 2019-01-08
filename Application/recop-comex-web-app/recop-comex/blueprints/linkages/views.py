from flask import Blueprint, render_template, redirect, url_for
from blueprints.linkages.forms import ProposalForm
from data_access.models import event_information, event_category
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

	form.category.choices = event_category.select()

	if form.validate_on_submit():
		id = event_information.count()
		value = [id,1,form.category.data,form.title.data,form.purpose.data,form.venue.data,form.date.data,1,"A"]
		event_information.add(value)
		return redirect(url_for('linkages.proposals'))

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