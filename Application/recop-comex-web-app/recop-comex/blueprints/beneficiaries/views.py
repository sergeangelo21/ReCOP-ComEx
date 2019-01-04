from flask import Blueprint, render_template
import os

beneficiaries = Blueprint('beneficiaries', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@beneficiaries.route('/beneficiaries')
def index():

	return render_template('/beneficiaries/index.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/events')
def events():

	return render_template('/beneficiaries/events.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/reports')
def reports():

	return render_template('/beneficiaries/reports.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/contactus')
def contactus():

	return render_template('/beneficiaries/contactus.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/termsandconditions')
def termsandconditions():

	return render_template('/beneficiaries/termsandconditions.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/profile')
def profile():

	return render_template('/beneficiaries/profile.html', title="Beneficiaries")
