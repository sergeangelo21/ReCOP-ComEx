from flask import Blueprint, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from data_access.models import *
from data_access.queries import *

from extensions import db

import os

admin = Blueprint('admin', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@admin.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))
		elif current_user.type == 4:
			return redirect(url_for('beneficiaries.index'))

@admin.route('/admin')
@login_required
def index():

	return render_template('/admin/index.html', title="Admin")

@admin.route('/admin/events')
@login_required
def events():

	return render_template('/admin/events.html', title="Events | Admin")

@admin.route('/admin/proposals/<status>')
@login_required
def proposals(status):

	return render_template('/admin/proposals/index.html', title="Proposals | Admin")

@admin.route('/admin/partners')
@login_required
def partners():

	partners = partner_views.show_all()

	return render_template('/admin/partners/index.html', title="Partners | Admin", partners=partners)

@admin.route('/admin/partners/show/id=<id>')
@login_required
def partner_show(id):

	partner, mem_since = partner_views.show_info(id)

	return render_template('/admin/partners/show.html', title="Partners | Admin", partner=partner, mem_since = mem_since)

@admin.route('/admin/partners/action/<name><id><status>')
@login_required
def partner_action(id, name, status):

	if status == "A":
		status = "D"
		flash(name + " was disabled!")
	else:

		if status=='N':
			new = 'MOA was sent to email.'
			status = "P"
		else:
			new = ''
			status = "A"

		flash(name + " was activated! " + new)

	user = user_account.update_status([id, status])

	audit_id = audit_trail.count()

	value = [audit_id,id,'partner',1]

	audit_trail.add(value)

	return redirect(url_for('admin.partners'))

@admin.route('/admin/beneficiaries')
@login_required
def beneficiaries():

	return render_template('/admin/beneficiaries.html', title="Beneficiaries | Admin")

@admin.route('/admin/reports')
@login_required
def reports():

	return render_template('/admin/reports.html', title="Reports | Admin")

@admin.route('/admin/feedbacks')
@login_required
def feedbacks():

	return render_template('/admin/feedbacks.html', title="Feedbacks | Admin")

@admin.route('/admin/profile')
@login_required
def profile():

	return render_template('/admin/profile.html', title="Profile | Admin")
