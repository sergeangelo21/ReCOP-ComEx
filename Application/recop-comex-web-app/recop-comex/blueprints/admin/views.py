from flask import Blueprint, render_template, url_for, redirect
from flask_login import current_user, login_required
from data_access.models import user_account, user_information
from data_access.queries import partners_view

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

@admin.route('/admin/proposals')
@login_required
def proposals():

	return render_template('/admin/proposals.html', title="Proposals | Admin")

@admin.route('/admin/partners')
@login_required
def partners():

	partners = partners_view()

	if partners is None:

		return 'None'

	return render_template('/admin/partners/index.html', title="Partners | Admin", partners=partners)

@admin.route('/admin/partners/show/<partners>')
@login_required
def partners_show(partners):

	partners = user_account.query.join(
		user_information
		).add_columns(
		user_information.id,
		user_information.first_name,
		user_information.middle_name,
		user_information.last_name,
		user_information.company_name,
		user_information.gender,
		user_information.birthday,
		user_information.address,
		user_information.telephone,
		user_information.mobile_number,
		user_account.status,
		).filter(user_account.id==partners
		).first()

	return render_template('/admin/partners/show.html', title="Partners | Admin", partners=partners)

@admin.route('/admin/partners/action/<partners>')
@login_required
def partners_action(partners):

	action = user_account.query.filter(user_account.id==partners).first()

	if action.status == "A":
		action.status = "D"
		db.session.commit()

	elif action.status == "D":
		action.status = "A"
		db.session.commit()

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
