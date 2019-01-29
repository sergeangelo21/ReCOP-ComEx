#Table specifications and simple queries goes here
from extensions import login, db, bcrypt
from flask_login import UserMixin, current_user

from datetime import datetime

@login.user_loader
def load_user(id):
	return user_account.query.get((id))

class audit_trail(db.Model):

	id = db.Column(db.INT, primary_key=True)
	user_id = db.Column(db.INT, db.ForeignKey('user_account.id'), nullable=False)
	affected_id = db.Column(db.INT, nullable=False)
	target = db.Column(db.VARCHAR(25), nullable=False)
	date_created = db.Column(db.DATETIME, nullable=False)
	type = db.Column(db.INT, nullable=False)

	def count():

		rows = db.session.query(audit_trail).count()
		rows+=1
		return rows

	def add(value):

		record = audit_trail(
			id = value[0],
			user_id	= current_user.id,
			affected_id = value[1],
			target = value[2],
			date_created = datetime.now(),
			type = value[3])

		db.session.add(record)
		db.session.commit()

class beneficiary(db.Model):

	id = db.Column(db.INT, primary_key=True)
	donor_id = db.Column(db.INT,db.ForeignKey('user_information.id'), nullable=False)
	beneficiary_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	budget = db.Column(db.NUMERIC(10,2))
	status = db.Column(db.CHAR(1), nullable=False)

class donation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	sponsee_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	sponsor_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	amount = db.Column(db.NUMERIC(10,2), nullable=False)
	date_given = db.Column(db.DATETIME, nullable=False)
	transaction_slip = db.Column(db.VARCHAR(200), nullable=False)
	is_event = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class event_attachment(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	path = db.Column(db.VARCHAR(200), nullable=False)
	type = db.Column(db.INT, nullable=False)

class event_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	organizer_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	name = db.Column(db.VARCHAR(30),nullable=False)
	description = db.Column(db.VARCHAR(140),nullable=False)
	objective = db.Column(db.VARCHAR(140),nullable=False)
	budget = db.Column(db.NUMERIC(10,2), nullable=False)
	location = db.Column(db.VARCHAR(50),nullable=False)
	event_date = db.Column(db.DATETIME, nullable=False)
	thrust = db.Column(db.INT, nullable=False)
	type = db.Column(db.INT, nullable=False)
	event_status = db.Column(db.CHAR(1), nullable=False)

	event_info_id = db.relationship('proposal_tracker', backref='event_information', lazy=True)

	def count():

		rows = db.session.query(event_information).count()
		rows+=1
		return rows

	def add(value):

		record = event_information(
			id=value[0], 
			organizer_id=value[1], 
			name=value[2], 
			description=value[3],
			objective=value[4],
			budget = value[5],
			location=value[6],
			event_date=value[7],
			thrust=value[8], 
			type=value[9],
			event_status=value[10]
			)
			 
		db.session.add(record)
		db.session.commit()

class event_participation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	participant_id = db.Column(db.INT)
	rating = db.Column(db.INT, nullable=False)
	comment = db.Column(db.VARCHAR(140),nullable=False)
	is_target = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class event_resource(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(30), nullable=False)
	type = db.Column(db.INT, nullable=False)

class proposal_tracker(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT, db.ForeignKey('event_information.id'), nullable=False)
	proposed_on = db.Column	(db.DATETIME, nullable=False)
	recop_accepted = db.Column(db.DATETIME)
	fmi_signed = db.Column(db.DATETIME)
	acad_signed = db.Column(db.DATETIME)
	approved_on = db.Column(db.DATETIME)
	comment = db.Column(db.VARCHAR(20))
	status = db.Column(db.CHAR(1), nullable=False)	

	def count():

		rows = db.session.query(proposal_tracker).count()
		rows+=1
		return rows

	def add(value):

		record = proposal_tracker(
			id = value[0],
			event_id = value[1],
			proposed_on = datetime.now(),
			recop_accepted = None,
			fmi_signed = None,
			acad_signed = None,
			approved_on = None,
			comment = None,
			status = 'N')

		db.session.add(record)
		db.session.commit()

class referral(db.Model):

	id = db.Column(db.INT, primary_key=True)
	referrer_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(50),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	type = db.Column(db.INT, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class user_account(db.Model, UserMixin):

	id = db.Column(db.INT, primary_key=True)
	info_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	username = db.Column(db.VARCHAR(20),nullable=False)
	password = db.Column(db.VARCHAR(20),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	type = db.Column(db.INT, nullable=False)
	last_active = db.Column(db.DATETIME, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	audit_account_id = db.relationship('audit_trail', backref='user_account', lazy=True)

	def count():

		rows = db.session.query(user_account).count()
		rows+=1
		return rows

	def add(value):

		record = user_account(
			id=value[0], 
			info_id=value[1],
			username=value[2],
			password= bcrypt.generate_password_hash(value[3]).decode('utf-8'),
			email_address=value[4],
			type=value[5],
			last_active=value[6],
			status=value[7]
			)
			 
		db.session.add(record)
		db.session.commit()

	def retrieve_user(value):

		user = user_account.query.filter(user_account.id==value).first()

		return user

	def update_status(id, status):

		user = user_account.query.filter(user_account.id==id).first()
		user.status = status
		db.session.commit()

	def login(value):

		user = user_account.query.filter(user_account.username==value[0]).first()

		if user:

			password = bcrypt.check_password_hash(user.password.encode('utf-8'), value[1].encode('utf-8'))

			if password==False:
				user = None

		return user

	def logout():

		user = user_account.query.filter(user_account.id==current_user.id).first()

		user.last_active = datetime.now()

		db.session.commit()

class user_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	first_name = db.Column(db.VARCHAR(30),nullable=False)
	middle_name = db.Column(db.VARCHAR(20),nullable=False)
	last_name = db.Column(db.VARCHAR(20),nullable=False)
	company_name = db.Column(db.VARCHAR(50),nullable=False)
	bio = db.Column(db.VARCHAR(160),nullable=True)
	gender = db.Column(db.CHAR(1), nullable=False)
	birthday = db.Column(db.DATE, nullable = False)
	address = db.Column(db.VARCHAR(50),nullable=False)
	telephone = db.Column(db.VARCHAR(15))
	mobile_number = db.Column(db.VARCHAR(15))
	partner_thrust = db.Column(db.INT, nullable=False)

	account_info_id = db.relationship('user_account', backref = 'user_information', lazy = True)
	sponsee_info_id = db.relationship('donation', foreign_keys=[donation.sponsee_id], backref='user_information_sponsee', lazy=True)
	sponsor_info_id = db.relationship('donation', foreign_keys=[donation.sponsor_id], backref='user_information_sponsor', lazy=True)
	donor_info_id = db.relationship('beneficiary', foreign_keys=[beneficiary.donor_id], backref='user_information_donor', lazy=True)
	bene_info_id = db.relationship('beneficiary', foreign_keys=[beneficiary.beneficiary_id], backref='user_information_bene', lazy=True)
	organizer_info_id = db.relationship('event_information', backref='user_information', lazy=True)

	def count():

		rows = db.session.query(user_information).count()
		rows+=1
		return rows

	def add(value):

		record = user_information(
			id=value[0], 
			first_name=value[1],
			middle_name=value[2],
			last_name=value[3],
			company_name=value[4],
			bio = value[5],
			gender=value[6],
			birthday = value[7],
			address=value[8],
			telephone=value[9],
			mobile_number=value[10],
			partner_thrust = value[11]
			)
			 
		db.session.add(record)
		db.session.commit()