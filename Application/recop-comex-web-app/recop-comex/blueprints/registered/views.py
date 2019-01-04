from flask import Blueprint, render_template
import os

registered = Blueprint('registered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@registered.route('/registered')
def index():

	return render_template('/registered/index.html')

@registered.route('/registered/events')
def events():

	return render_template('/registered/events.html')

@registered.route('/registered/partners')
def partners():

	return render_template('/registered/partners.html')

@registered.route('/registered/donate')
def donate():

	return render_template('/registered/donate.html')

@registered.route('/registered/contactus')
def contactus():

	return render_template('/registered/contactus.html')

@registered.route('/registered/termsandservices')
def termsandservices():

	return render_template('/registered/termsandservices.html')

@registered.route('/registered/profile')
def profile():

	return render_template('/registered/profile.html')