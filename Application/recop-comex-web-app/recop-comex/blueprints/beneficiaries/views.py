from flask import Blueprint, render_template
from flask_login import login_required
import os

beneficiaries = Blueprint('beneficiaries', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@beneficiaries.route('/beneficiaries')
@login_required
def index():

	return render_template('/beneficiaries/index.html', title="Beneficiaries")

@beneficiaries.route('/beneficiaries/events')
@login_required
def events():

	return render_template('/beneficiaries/events.html', title="Beneficiaries")

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
