from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from blueprints.linkages.forms import *
from data_access.models import user_account, event_information, event_participation, proposal_tracker, user_information
from data_access.queries import user_views, community_views

from extensions import db, bcrypt
import os

linkages = Blueprint('linkages', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@linkages.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 4:
			return redirect(url_for('communities.index'))

@linkages.route('/linkages/index')
@login_required
def index():

	return render_template('/linkages/index.html')

@linkages.route('/linkages/events')
@login_required
def events():

	events = event_information.query.all()

	return render_template('/linkages/events/index.html', events=events)

@linkages.route('/linkages/events/create', methods=['GET','POST'])
@login_required
def events_create():

	form = ProposalForm()

	communities = community_views.target_community()

	form.select_comm.choices.extend([(c.id,c.address) for c in communities])

	if form.validate_on_submit():

		det = user_information.linkage_info(current_user.info_id)

		if det.company_name=='San Sebastian College Recoletos de Cavite':
			event_type=1
		else:
			event_type=2

		event_id = event_information.count()
		
		value = [
		event_id,current_user.info_id,form.title.data,
		form.description.data,form.objective.data,form.budget.data,form.location.data,
		form.event_date.data,form.thrust.data,event_type,'N'
		]

		event_information.add(value)

		if form.target_comm.data:

			comm = form.target_comm.data.split('|',-1)

			for participant in comm:

				if participant!='':
					id = event_participation.count()
					value = [id, event_id, participant, 'Y']
					event_participation.add(value)

		id = proposal_tracker.count()
		value = [id, event_id]
		proposal_tracker.add(value)

		flash('Event proposal submitted! Please standby for the approval.', 'success')

		return redirect(url_for('linkages.events'))

	return render_template('/linkages/events/create.html', form=form)

@linkages.route('/linkages/communities')
@login_required
def communities():

	return render_template('/linkages/communities/index.html')

@linkages.route('/linkages/reports')
@login_required
def reports():

	return render_template('/linkages/reports/index.html')

@linkages.route('/linkages/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/linkages/termsandconditions/index.html')

@linkages.route('/linkages/profile/about/<user>')
@login_required
def profile_about(user):

	linkages = user_views.profile_info(current_user.info_id)

	return render_template('/linkages/profile/about.html', linkages=linkages)	

@linkages.route('/linkages/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/linkages/profile/eventsattended.html')	

@linkages.route('/linkages/profile/settings')
@login_required
def profile_settings():

	return render_template('/linkages/profile/settings.html')	

@linkages.route('/linkages/profile/update/<user>', methods=['GET', 'POST'])
@login_required
def profile_update(user):

	user_information_update = user_views.profile_info_update(current_user.info_id)
	user_account_update = user_views.profile_acc_update(current_user.info_id)

	form = ProfileUpdateForm()

	if form.validate_on_submit():

		if user:

			user_information_update.first_name = form.firstname.data
			user_information_update.middle_name = form.middlename.data
			user_information_update.last_name = form.lastname.data
			user_information_update.gender = form.gender.data
			user_information_update.birthday = form.birthday.data
			user_information_update.bio = form.bio.data

			user_information_update.company_name = form.company.data
			user_information_update.address = form.address.data
			user_information_update.telephone = form.telephone.data
			user_information_update.mobile_number = form.mobile.data

			db.session.commit()

			user_account_update.email_address = form.email.data

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Profile was successfully updated!', 'success')

			return redirect(url_for('linkages.profile_about', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio
		
		form.company.data = user_information_update.company_name
		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

		form.username.data = user_account_update.username

	return render_template('/linkages/profile/update.html', form=form)

@linkages.route('/linkages/profile/updatepassword/<user>', methods=['GET', 'POST'])
@login_required
def profile_update_password(user):

	user_account_update = user_views.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('linkages.profile_about', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	return render_template('/linkages/profile/update_password.html', form=form)