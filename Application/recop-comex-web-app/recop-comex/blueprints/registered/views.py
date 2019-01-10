from flask import Blueprint, render_template
from flask_login import login_required
import os

registered = Blueprint('registered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# @registered.before_request
# def before_request():
# 	if current_user.is_authenticated and not current_user.is_anonymous:

@registered.route('/registered')
@login_required
def index():

	return render_template('/registered/index.html')

@registered.route('/registered/events')
@login_required
def events():

	return render_template('/registered/events.html')

@registered.route('/registered/partners')
@login_required
def partners():

	return render_template('/registered/partners.html')

@registered.route('/registered/donate')
@login_required
def donate():

	return render_template('/registered/donate.html')

@registered.route('/registered/contactus')
@login_required
def contactus():

	return render_template('/registered/contactus.html')

@registered.route('/registered/termsandservices')
@login_required
def termsandservices():

	return render_template('/registered/termsandservices.html')

@registered.route('/registered/profile')
@login_required
def profile():

	return render_template('/registered/profile.html')