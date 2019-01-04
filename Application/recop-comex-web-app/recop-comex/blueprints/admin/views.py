from flask import Blueprint, render_template
import os

admin = Blueprint('admin', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@admin.route('/admin')
def index():

	return render_template('/admin/index.html', title="Admin")

@admin.route('/admin/events')
def events():

	return render_template('/admin/events.html', title="Admin")

@admin.route('/admin/proposals')
def proposals():

	return render_template('/admin/proposals.html', title="Admin")

@admin.route('/admin/partners')
def partners():

	return render_template('/admin/partners.html', title="Admin")

@admin.route('/admin/beneficiaries')
def beneficiaries():

	return render_template('/admin/beneficiaries.html', title="Admin")

@admin.route('/admin/reports')
def reports():

	return render_template('/admin/reports.html', title="Admin")

@admin.route('/admin/feedbacks')
def feedbacks():

	return render_template('/admin/feedbacks.html', title="Admin")

@admin.route('/admin/profile')
def profile():

	return render_template('/admin/profile.html', title="Admin")
