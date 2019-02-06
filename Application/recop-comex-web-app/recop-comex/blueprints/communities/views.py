from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from blueprints.communities.forms import *
from data_access.models import user_account, user_information, proposal_tracker, event_information
from data_access.queries import user_views, linkage_views

from extensions import db, bcrypt
import os

communities = Blueprint('communities', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@communities.before_request
def before_request():

	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 1:
			return redirect(url_for('admin.index'))
		elif current_user.type == 2:
			return redirect(url_for('registered.index'))
		elif current_user.type == 3:
			return redirect(url_for('linkages.index'))

@communities.route('/communities')
@login_required
def index():

	return render_template('/communities/index.html', title="Communities")

@communities.route('/communities/events')
@login_required
def events():

	events = event_information.query.all()

	return render_template('/communities/events/index.html', title="Communities", events=events)

@communities.route('/communities/linkages/filter_<search>', methods=['GET', 'POST'])
@login_required
def linkages(search):


	linkages = linkage_views.show_list('A', 3, search=search)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('communities.linkages', search=form.search.data))

	return render_template('/communities/linkages/index.html', title="Communities", form=form, linkages=linkages, search=search)

@communities.route('/communities/linkages/show/id=<id>')
@login_required
def linkage_show(id):

	linkage, mem_since = linkage_views.show_info(id)

	return render_template('/communities/linkages/show.html', title= linkage.company_name.title() + " | Admin", linkage=linkage)

@communities.route('/communities/reports')
@login_required
def reports():

	return render_template('/communities/reports/index.html', title="Communities")

@communities.route('/communities/contactus')
@login_required
def contactus():

	return render_template('/communities/contactus/index.html', title="Communities")

@communities.route('/communities/termsandconditions')
@login_required
def termsandconditions():

	return render_template('/communities/termsandconditions/index.html', title="Communities")

@communities.route('/communities/profile/about/<user>')
@login_required
def profile_about(user):

	communities = user_views.profile_info(current_user.info_id)

	return render_template('/communities/profile/about.html', title="Communities", communities=communities)

@communities.route('/communities/profile/eventsattended')
@login_required
def profile_eventsattended():

	return render_template('/communities/profile/eventsattended.html', title="Communities")	

@communities.route('/communities/profile/settings/personal', methods=['GET', 'POST'])
@login_required
def profile_settings_personal():

	user_information_update = user_information.profile_info_update(current_user.info_id)

	form = ProfilePersonalUpdateForm()

	if form.validate_on_submit():

		user_information_update.first_name = form.firstname.data
		user_information_update.middle_name = form.middlename.data
		user_information_update.last_name = form.lastname.data
		user_information_update.gender = form.gender.data
		user_information_update.birthday = form.birthday.data
		user_information_update.bio = form.bio.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('communities.profile_settings_personal'))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/communities/profile/settings/personal.html', title="Communities", form=form)

@communities.route('/communities/profile/settings/contact', methods=['GET', 'POST'])
@login_required
def profile_settings_contact():

	user_information_update = user_information.profile_info_update(current_user.info_id)
	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileContactUpdateForm()

	if form.validate_on_submit():

		user_information_update.address = form.address.data
		user_information_update.telephone = form.telephone.data
		user_information_update.mobile_number = form.mobile.data

		db.session.commit()

		user_account_update.email_address = form.email.data

		db.session.commit()

		flash('Profile was successfully updated!', 'success')

		return redirect(url_for('communities.profile_settings_contact'))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/communities/profile/settings/contact.html', title="Communities", form=form)	

@communities.route('/communities/profile/settings/username', methods=['GET', 'POST'])
@login_required
def profile_settings_username():

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('communities.profile_settings_username'))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/communities/profile/settings/username.html', title="Communities", form=form)

@communities.route('/communities/profile/update/password', methods=['GET', 'POST'])
@login_required
def profile_settings_password():

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('communities.profile_settings_password'))

		else:

			flash('Wrong password.', 'error')

	return render_template('/communities/profile/settings/password.html', title="Communities", form=form)