from flask import Blueprint, render_template, redirect, url_for, flash, send_from_directory, request
from flask_login import current_user, logout_user, login_required
from blueprints.linkages.forms import *
from data_access.models import user_account, event_information, event_participation, proposal_tracker, user_information, event_attachment, event_photo, donation, referral, user_photo
from data_access.queries import user_views, linkage_views, event_views, donation_views
from extensions import db, bcrypt
from static.email import generate, send_email
from static.pdf import generate_pdf
from datetime import datetime

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
		elif current_user.type == 5:
			return redirect(url_for('religious_admin.index'))
		user_account.logout()

@linkages.route('/linkages/index')
@login_required
def index():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/linkages/index.html', photo=photo, active='home')

@linkages.route('/linkages/events/<status>/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def events(status, search, page):

	if status=='scheduled':
		value='S'
	elif status=='new':
		value='N'
	elif status=='pending':
		value='P'
	elif status=='cancelled':
		value='C'
	elif status=='declined':
		value='X'
	elif status=='finished':
		value='F'
	else:
		value=status

	events = event_views.linkages_events([value, search, page])
	letters = event_attachment.letter_attached()
	
	photo = user_photo.photo(current_user.info_id)

	form = AttachLetterForm()

	if form.validate_on_submit():

		attach_letter = form.attach_letter.data
		old, extension = os.path.splitext(attach_letter.filename)
		filename = str(form.event_id.data)+extension
		file_path = 'static/attachment/signed_letter/' + filename

		value = [None,form.event_id.data,file_path,3]

		event_attachment.add(value)
		attach_letter.save(file_path)

		flash('Letter successfully attached!', 'success')

		return redirect(url_for('linkages.events', status=status, page='1', search=' '))

	form_search = SearchForm()

	if form_search.validate_on_submit():

		return redirect(url_for('linkages.events', status=status, page='1', search=form_search.search.data))

	return render_template('/linkages/events/index.html', title="Events", form_search=form_search, form=form, events=events, status=status, letters=letters, now=datetime.now(), search=search, photo=photo, active='events')

@linkages.route('/linkages/events/calendar', methods=['GET', 'POST'])
@login_required
def events_calendar():

	photo = user_photo.photo(current_user.info_id)

	events = event_information.calendar()
	
	return render_template('/linkages/events/index-calendar.html', title="Events", events=events, photo=photo, active='events')
	
@linkages.route('/linkages/events/show/<id>')
@login_required
def event_show(id):

	event = event_views.show_info(id)
	participants = event_views.show_participants([id,' '])

	form=SearchForm()

	return render_template('/linkages/events/show.html', title= event.name.title() , event = event, participants=participants,form=form, active='events')

@linkages.route('/linkages/events/conduct/<id>')
@login_required
def event_conduct(id):

	event = event_views.show_info(id)

	return render_template('/linkages/events/conduct.html', title= event.name.title() ,event=event, active='events')

@linkages.route('/linkages/events/photos/<id>', methods=['GET', 'POST'])
@login_required
def event_photos(id):

	event = event_views.show_info(id)

	photos  = event_photo.show(id)

	form = CaptionForm()

	if form.validate_on_submit():

		value = [form.photo.data, form.caption.data]
		event_photo.caption(value)
		flash('Caption added to photo!', 'success')
		return redirect(url_for('linkages.event_photos', id=event.id))

	return render_template('/linkages/events/photos.html', title= event.name.title() ,event=event, photos=photos, form=form, active='events')

@linkages.route('/linkages/events/photos/add/<id>', methods=['GET', 'POST'])
@login_required
def add_photos(id):

	event = event_views.show_info(id)
	form = PhotoForm()

	print()
	if form.validate_on_submit():

		for file in form.photos.data:

			old, extension = os.path.splitext(file.filename)

			extension = extension.lower()
			
			if extension==".jpg" or extension==".jpeg" or extension==".png" or extension==".gif":
				continue
			else:
				flash('Invalid file detected!', 'error')
				return redirect(url_for('linkages.add_photos', id=id))

		path = 'static/photos/events/'+id

		if not os.path.isdir(path):
			os.mkdir(path)

		for file in form.photos.data:

			old, extension = os.path.splitext(file.filename)
			filepath = path + '/' + file.filename
			file.save(filepath)

			value = [None, id, filepath, None, 'Y']
			event_photo.add(value)

		flash('Photos successfully uploaded!', 'success')
		return redirect(url_for('linkages.event_photos', id=id))

	return render_template('/linkages/events/add_photos.html', title= event.name.title() ,event=event, form=form, active='events')

@linkages.route('/linkages/events/photos/delete/<id>_from_<event>', methods=['GET', 'POST'])
@login_required
def delete_photo(id, event):

	event_photo.delete(id)

	flash('Photo was deleted!', 'success')

	return redirect(url_for('linkages.event_photos', id=event))

@linkages.route('/linkages/events/finish/<id>')
@login_required
def event_finish(id):

	event_information.update_status(id, 'F')
	flash('Event was finished! Kindly submit activity photos to complete the report.','success')

	return redirect(url_for('linkages.events', status='all', search=' ', page='1'))

@linkages.route('/linkages/events/attendance/<id>.search_<search>', methods=['GET', 'POST'])
@login_required
def event_attendance(id, search):

	event = event_views.show_info(id)
	participants = event_views.show_participants([id,search])

	form=SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('linkages.event_attendance', id=id, search=form.search.data))

	return render_template('/linkages/events/attendance.html', title= event.name.title() ,event=event,participants=participants,form=form, search=search, active='events')

@linkages.route('/linkages/events/attendance/<id>/<action>.user_<user>')
@login_required
def attendance_action(id, action, user):

	if action=='present':

		event_participation.update([id,user,'P'])
		flash('Participant was marked as present!', 'success')

	if action=='absent':

		event_participation.update([id,user,'A'])
		flash('Participant was marked as absent!', 'success')

	return redirect(url_for('linkages.event_attendance', id=id, search=' '))

@linkages.route('/linkages/events/evaluation/<id>.search_<search>', methods=['GET', 'POST'])
@login_required
def event_evaluation(id, search):

	event = event_views.show_info(id)
	participants = event_views.show_attended([id,search])

	form=SearchForm()
	evaluate = EvaluationForm()

	if form.validate_on_submit():

		return redirect(url_for('linkages.event_evaluation', id=id, search=form.search.data))

	if evaluate.validate_on_submit():

		print(evaluate.participant.data)
		event_participation.evaluate([event.id, evaluate.participant.data, evaluate.rating.data, evaluate.comment.data])
		
		flash('Rating successfully submitted!', 'success')
		return redirect(url_for('linkages.event_evaluation', id=id, search=search))


	return render_template('/linkages/events/evaluation.html', title= event.name.title() ,event=event,participants=participants,form=form, evaluate = evaluate, search=search, active='events')

@linkages.route('/linkages/events/create', methods=['GET', 'POST'])
@login_required
def events_create():

	form = ProposalForm()

	linkages = linkage_views.target_linkages()

	for item in linkages:

		if item.type==3:
			name = item.company_name
		else:
			name = item.address

		form.select_link.choices.extend([(item.id, name)])

	if form.validate_on_submit():

		det = user_information.linkage_info(current_user.info_id)

		if det.company_name=='San Sebastian College Recoletos de Cavite':
			event_type=1
		else:
			event_type=2

		value = [
		None,current_user.info_id,form.title.data,
		form.description.data,form.objective.data,form.budget.data,form.location.data,
		form.event_date.data,form.participant_no.data, form.min_age.data, form.max_age.data,
		form.thrust.data,event_type,'N'
		]

		event_information.add(value)

		event = event_information.last_added(current_user.id)

		if form.target_link.data:

			comm = form.target_link.data.split('|',-1)

			for participant in comm:

				if participant!='':
					value = [None, event.id, participant, 'Y']
					event_participation.add(value)

		budget_plan = form.budget_plan.data
		old, extension = os.path.splitext(budget_plan.filename)
		filename = str(event.id)+extension
		file_path = 'static/attachment/budget_plan/' + filename

		value = [None,event.id,file_path,1]

		event_attachment.add(value)
		budget_plan.save(file_path)

		programme = form.programme.data
		old, extension = os.path.splitext(programme.filename)
		filename = str(event.id)+extension
		file_path = 'static/attachment/programme/' + filename

		value = [None,event.id,file_path,2]

		event_attachment.add(value)
		programme.save(file_path)

		value = [None, event.id, 'N']
		proposal_tracker.add(value)

		flash('Event proposal submitted! Please wait for the approval.', 'success')

		return redirect(url_for('linkages.events', status='all', page='1', search=' '))

	return render_template('/linkages/events/create.html', form=form, active='events')

@linkages.route('/linkages/events/reschedule/id=<id>', methods=['GET', 'POST'])
@login_required
def event_reschedule(id):

	form = RescheduleEventForm()

	resched_event = event_information.reschedule(id)

	if form.validate_on_submit():

		resched_event.location = form.location.data
		resched_event.event_date = form.event_date.data

		db.session.commit()

		flash('Event rescheduled!', 'success')

		return redirect(url_for('linkages.events', status='all', page='1', search=' '))

	else:

		form.location.data = resched_event.location
		form.event_date.data = resched_event.event_date

	return render_template('/linkages/events/reschedule.html', title="Reschedule", form=form, event=resched_event, active='events')

@linkages.route('/linkages/events/<action>/id=<id>')
@login_required
def event_action(id, action):

	event = event_information.retrieve_event(id)

	if action=='cancel':

		status='C'
		proposal_tracker.update_status(event.id, status)
		event_information.update_status(event.id, status)

		value = [None,current_user.id,event.id,'event', 8]
		audit_trail.add(value)

		flash(event.name + ' was cancelled.', 'success')	

	return redirect(url_for('linkages.events', status='all', page='1', search=' '))

@linkages.route('/linkages/events/letter/<id>_<name>', methods=['GET', 'POST'])
@login_required
def event_letter(id, name):

	filepath = 'static/output/events/letters/'

	event = event_views.show_info(id)
	admin = user_information.retrieve_user(1)

	html = render_template('linkages/pdf/pdf.html', event=event, admin=admin, date = datetime.now())

	generate_pdf(html, filepath + str(id) + '.pdf')

	return send_from_directory(filepath, str(id) +'.pdf')

@linkages.route('/linkages/events/stream/<id>')
@login_required
def event_stream(id):

	return render_template('linkages/events/stream.html', id=id)

@linkages.route('/linkages/linkages/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def linkages_show(page, search):

	linkages = linkage_views.show_list(['A', search, 3, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('linkages.linkages_show', page='1', search=form.search.data))

	return render_template('/linkages/linkages/index.html', linkages=linkages, form = form, search=search, user=current_user.info_id, photo=photo, active='linkages')

@linkages.route('/linkages/communities/search_<search>.page_<page>', methods=['GET', 'POST'])
@login_required
def communities(page, search):

	communities = linkage_views.show_list(['all',search,4, page])

	photo = user_photo.photo(current_user.info_id)

	form = SearchForm()

	if form.validate_on_submit():

		return redirect(url_for('linkages.communities', page='1', search=form.search.data))

	return render_template('/linkages/communities/index.html', form=form, communities=communities, search=search, photo=photo, active='communities')

@linkages.route('/linkages/donate', methods=['GET', 'POST'])
@login_required
def donate():

	photo = user_photo.photo(current_user.info_id)

	form = DonationForm()

	communities = linkage_views.target_linkages()

	donations = donation_views.donation_history(current_user.info_id)

	for c in communities:

		if c.type==4:
			form.sponsee.choices.extend([(str(c.id), c.address)])

	events = event_information.select_list()

	if events:

		for e in events:
			form.event.choices.append((str(e.id), e.name))
			no_event = 0

	else: 
		
		form.event.data=''
		no_event = 1

	if form.validate_on_submit():

		if form.give_to.data=='1':
			if form.sponsee.data:
				sponsee = form.sponsee.data
			else:
				sponsee = 1

			event = None
		else:
			event = form.event.data
			sponsee= None

		file = form.trans_slip.data
		old, extension = os.path.splitext(file.filename)

		new = donation.last_added()
		filename = str(new)+extension

		trans_path = 'static/output/donate/trans_slip/' + filename

		value = [None,sponsee,event,current_user.info_id,form.amount.data,trans_path,'N']

		donation.add(value)
		file.save(trans_path)

		flash('Donation given!', 'success')
		return redirect(url_for('linkages.donate'))

	return render_template('/linkages/donate/index.html', form=form, no_event=no_event, donations=donations, photo=photo, active='donate')

@linkages.route('/linkages/referral', methods=['GET', 'POST'])
@login_required
def referral_users():

	form = ReferralForm()

	if form.validate_on_submit():

		html = 'asdlkfjasfd'
		subject = 'REFFERAL: '
		admin = user_account.retrieve_user(1)

		email_parts = [html, subject, admin.email_address, form.email.data, None]
		send_email(email_parts)

		value = [None, current_user.id, form.name.data, form.email.data, form.type.data, 'N']

		referral.add(value)

		flash('Referral has been sent!', 'success')
		return redirect(url_for('linkages.referral_users'))	

	return render_template('/linkages/referral/index.html', form=form, active='referral')

@linkages.route('/linkages/contactus')
@login_required
def contactus():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/linkages/contactus/index.html', photo=photo, active='contactus')

@linkages.route('/linkages/termsandconditions')
@login_required
def termsandconditions():

	photo = user_photo.photo(current_user.info_id)

	return render_template('/linkages/termsandconditions/index.html', photo=photo, active='termsandconditions')

@linkages.route('/linkages/profile/about|<user>', methods=['GET', 'POST'])
@login_required
def profile_about(user):

	linkages = user_views.profile_info(current_user.info_id)

	photo = user_photo.photo(current_user.info_id)
	form = PictureForm()

	if form.validate_on_submit():

		file = form.photo.data
		old, extension = os.path.splitext(file.filename)
		filename = str(current_user.info_id)+extension
		file_path = 'static/photos/profiles/' + filename

		file.save(file_path)

		if photo:
			user_photo.update([current_user.info_id, file_path])
		else:
			user_photo.add([None, current_user.info_id, file_path])

		flash('Profile picture has been updated!', 'success')
		return redirect(url_for('linkages.profile_about', user=user))

	return render_template('/linkages/profile/about.html', title="Linkages",  photo=photo, form=form, linkages=linkages)

@linkages.route('/linkages/profile/eventsattended|<user>')
@login_required
def profile_eventsattended(user):

	return render_template('/linkages/profile/eventsattended.html', title="Linkages")	

@linkages.route('/linkages/profile/settings/personal|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_personal(user):

	user_information_update = user_information.profile_info_update(current_user.info_id)

	photo = user_photo.photo(current_user.info_id)

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

		return redirect(url_for('linkages.profile_settings_personal', user=current_user.username))

	else:

		form.firstname.data = user_information_update.first_name
		form.middlename.data = user_information_update.middle_name
		form.lastname.data = user_information_update.last_name
		form.gender.data = user_information_update.gender
		form.birthday.data = user_information_update.birthday
		form.bio.data = user_information_update.bio

	return render_template('/linkages/profile/settings/personal.html', title="Linkages", form=form, photo=photo)

@linkages.route('/linkages/profile/settings/contact|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_contact(user):

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

		return redirect(url_for('linkages.profile_settings_contact', user=current_user.username))

	else:

		form.address.data = user_information_update.address
		form.telephone.data = user_information_update.telephone
		form.mobile.data = user_information_update.mobile_number
		form.email.data = user_account_update.email_address

	return render_template('/linkages/profile/settings/contact.html', title="Linkages", form=form)	

@linkages.route('/linkages/profile/settings/username|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_username(user):

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = ProfileUsernameUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.username = form.username.data

			db.session.commit()

			flash('Username was successfully updated!', 'success')

			return redirect(url_for('linkages.profile_settings_username', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	else:

		form.username.data = user_account_update.username

	return render_template('/linkages/profile/settings/username.html', title="Linkages", form=form)

@linkages.route('/linkages/profile/settings/password|<user>', methods=['GET', 'POST'])
@login_required
def profile_settings_password(user):

	user_account_update = user_account.profile_acc_update(current_user.info_id)

	form = PasswordUpdateForm()

	if form.validate_on_submit():

		user = user_account.login([current_user.username, form.oldpassword.data])

		if user:

			user_account_update.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

			db.session.commit()

			flash('Password was successfully updated!', 'success')

			return redirect(url_for('linkages.profile_settings_password', user=current_user.username))

		else:

			flash('Wrong password.', 'error')

	return render_template('/linkages/profile/settings/password.html', title="Linkages", form=form)

@linkages.route('/logout/linkages')
def logout():

	user_account.logout()

	logout_user()

	flash('You are logged out.', 'success')

	return redirect('/')