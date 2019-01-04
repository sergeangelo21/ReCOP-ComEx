from flask import Blueprint, render_template
import os

linkages = Blueprint('linkages', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@linkages.route('/linkages')
def index():

	return render_template('/linkages/index.html')

@linkages.route('/linkages/events')
def events():

	return render_template('/linkages/events.html')

@linkages.route('/linkages/proposals')
def proposals():

	return render_template('/linkages/proposals.html')

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