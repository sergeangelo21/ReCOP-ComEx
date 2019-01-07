#Table specifications and simple queries goes here

from extensions import db

class audit_trail(db.Model):

	id = db.Column(db.INT, primary_key=True)
	user_id = db.Column(db.INT)
	affected_id = db.Column(db.INT, nullable=False)
	target_table = db.Column(db.VARCHAR(25), nullable=False)
	date_created = db.Column(db.DATETIME, nullable=False)
	type = db.Column(db.CHAR(1), nullable=False)

class beneficiary(db.Model):

	id = db.Column(db.INT, primary_key=True)
	donor_id = db.Column(db.INT)
	beneficiary_id = db.Column(db.INT)
	budget = db.Column(db.NUMERIC(10,2))
	status = db.Column(db.CHAR(1), nullable=False)

class donation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	sponsee_id = db.Column(db.INT)
	sponsor_id = db.Column(db.INT)
	amount = db.Column(db.NUMERIC(10,2), nullable=False)
	date_given = db.Column(db.DATETIME, nullable=False)
	transaction_slip = db.Column(db.VARCHAR(30), nullable=False)
	is_event = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class event_category(db.Model):

	id = db.Column(db.INT, primary_key=True)
	name = db.Column(db.VARCHAR(20), nullable=False)
	description = db.Column(db.VARCHAR(30), nullable=False)

class event_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	organizer_id = db.Column(db.INT)
	category_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(30),nullable=False)
	description = db.Column(db.VARCHAR(30),nullable=False)
	location = db.Column(db.VARCHAR(50),nullable=False)
	event_date = db.Column(db.DATETIME, nullable=False)
	type = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	def add(value):

		record = event_information(
			id=value[0], 
			organizer_id=value[1], 
			category_id=value[2], 
			name=value[3], 
			description=value[4],
			location=value[5],
			event_date=value[6],
			type=value[7],
			status=value[8]
			)
			 
		db.session.add(record)
		db.session.commit()

		return "hey"

	def show(status):

		result = event_information.query.filter(event_information.status==status).first()

		return result.name

class event_participation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT)
	participant_id = db.Column(db.INT)
	rating = db.Column(db.INT, nullable=False)
	comment = db.Column(db.VARCHAR(140),nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class event_signatory(db.Model):

	id = db.Column(db.INT, primary_key=True)
	signatory_id = db.Column(db.INT)
	description = db.Column(db.VARCHAR(20),nullable=False)
	order = db.Column(db.CHAR(1), nullable=False)

class referral(db.Model):

	id = db.Column(db.INT, primary_key=True)
	referrer_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(50),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	type = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class user_account(db.Model):

	id = db.Column(db.INT, primary_key=True)
	info_id = db.Column(db.INT)
	type_id = db.Column(db.INT)
	username = db.Column(db.VARCHAR(20),nullable=False)
	password = db.Column(db.VARCHAR(20),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	last_active = db.Column(db.DATETIME, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

class user_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	first_name = db.Column(db.VARCHAR(30),nullable=False)
	middle_name = db.Column(db.VARCHAR(20),nullable=False)
	last_name = db.Column(db.VARCHAR(20),nullable=False)
	company_name = db.Column(db.VARCHAR(50),nullable=False)
	gender = db.Column(db.CHAR(1), nullable=False)
	address = db.Column(db.VARCHAR(50),nullable=False)
	telephone = db.Column(db.VARCHAR(15))
	mobile_number = db.Column(db.VARCHAR(15))
	type = db.Column(db.CHAR(1), nullable=False)
	is_active = db.Column(db.CHAR(1), nullable=False)

class user_type(db.Model):

	id = db.Column(db.INT, primary_key=True)
	name = db.Column(db.VARCHAR(15),nullable=False)
	privileges = db.Column(db.VARCHAR(15),nullable=False)