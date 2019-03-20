#Table specifications and basic CRUD queries goes here
from extensions import login, db, bcrypt
from flask_login import UserMixin, current_user
from sqlalchemy import and_, or_, func

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

	def add(value):

		record = audit_trail(
			id = value[0],
			user_id	= value[1],
			affected_id = value[2],
			target = value[3],
			date_created = datetime.now(),
			type = value[4])

		db.session.add(record)
		db.session.commit()

class community_info(db.Model):

	id = db.Column(db.INT, primary_key=True)
	community_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	classification = db.Column(db.INT, nullable=False)
	population = db.Column(db.INT, nullable=False)
	economic = db.Column(db.VARCHAR(50), nullable=False)
	problem = db.Column(db.VARCHAR(50), nullable=False)
	need = db.Column(db.VARCHAR(50), nullable=False)

	def add(value):

		record = community_info(
			id = value[0],
			community_id = value[1],
			classification = value[2],
			population = value[3],
			economic = value[4],
			problem = value[5],
			need = value[6])

		db.session.add(record)
		db.session.commit()

	def show(value):

		record = community_info.query.filter(community_info.id==value).first()

		return record

class community_member(db.Model):

	id = db.Column(db.INT, primary_key=True)
	member_id = db.Column(db.INT,db.ForeignKey('user_information.id'), nullable=False)
	community_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	occupation = db.Column(db.VARCHAR(30), nullable=True)
	income = db.Column(db.NUMERIC(10,2), nullable=False)
	religion = db.Column(db.VARCHAR(20), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	def add(value):

		record = community_member(
			id = value[0],
			member_id = value[1],
			community_id = value[2],
			occupation = value[3],
			income = value[4],
			religion = value[5],
			status = value[6])

		db.session.add(record)
		db.session.commit()

	def retrieve_member(value):

		record = community_member.query.filter(community_member.member_id==value).first()

		return record

	def update_status(id, status):

		user = community_member.query.filter(community_member.id==id).first()
		user.status = status
		db.session.commit()

	def member_count():

		record = community_member.query.add_columns(
			community_member.community_id,
			func.COUNT(community_member.member_id).label('count')
			).group_by(community_member.community_id
			).all()

		return record

class donation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	sponsee_id = db.Column(db.INT, db.ForeignKey('user_information.id'))
	event_id = db.Column(db.INT, db.ForeignKey('event_information.id'))
	sponsor_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	amount = db.Column(db.NUMERIC(10,2), nullable=False)
	date_given = db.Column(db.DATETIME, nullable=False)
	transaction_slip = db.Column(db.VARCHAR(200), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	inventory_donation_id = db.relationship('inventory', backref='donation', lazy=True)

	def add(value):

		record = donation(
			id=value[0],
			sponsee_id=value[1],
			event_id=value[2],
			sponsor_id=value[3],
			amount=value[4],
			date_given=datetime.now(),
			transaction_slip=value[5],
			status=value[6])

		db.session.add(record)
		db.session.commit()

	def last_added():

		record = donation.query.count()

		record+=1

		return record

	def retrieve_donation(id):

		record = donation.query.filter_by(id=id).first()

		return record

	def update_status(value):

		record = donation.query.filter_by(id=value[0]).first()

		record.status=value[1]

		db.session.commit()

	def d_status():

		record = donation.query.add_columns(
			donation.status,
			func.COUNT(donation.id).label('count')
			).group_by(donation.status
			).all()

		return record		

class event_attachment(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT,  db.ForeignKey('event_information.id'), nullable=False)
	path = db.Column(db.VARCHAR(200), nullable=False)
	type = db.Column(db.INT, nullable=False)

	def add(value):

		record = event_attachment(
				id = value[0],
				event_id = value[1],
				path = value[2],
				type = value[3]
				)

		db.session.add(record)
		db.session.commit()

	def retrieve_files(value):

		record = event_attachment.query.filter(event_attachment.event_id==value).all()

		return record

	def letter_attached():

		record = event_attachment.query.filter(event_attachment.type==3).all()

		return record

class event_information(db.Model):

	id = db.Column(db.INT, primary_key=True)
	organizer_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	name = db.Column(db.VARCHAR(30),nullable=False)
	description = db.Column(db.VARCHAR(140),nullable=False)
	objective = db.Column(db.VARCHAR(140),nullable=False)
	budget = db.Column(db.NUMERIC(10,2), nullable=False)
	location = db.Column(db.VARCHAR(50),nullable=False)
	event_date = db.Column(db.DATETIME, nullable=False)
	participant_no = db.Column(db.INT, nullable=False)
	min_age = db.Column(db.INT, nullable=False)
	max_age = db.Column(db.INT, nullable=False)
	thrust = db.Column(db.INT, nullable=False)
	type = db.Column(db.INT, nullable=False)
	event_status = db.Column(db.CHAR(1), nullable=False)

	event_info_id = db.relationship('proposal_tracker', backref='event_information', lazy=True)
	event_part_id = db.relationship('event_participation', backref='event_information', lazy=True)
	event_att_id = db.relationship('event_attachment', backref='event_information', lazy=True)
	event_donate_id = db.relationship('donation', backref='event_information', lazy=True)
	event_photo_id = db.relationship('event_photo', backref='event_information', lazy=True)

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
			participant_no=value[8],
			min_age=value[9],
			max_age=value[10],
			thrust=value[11], 
			type=value[12],
			event_status=value[13]
			)
			 
		db.session.add(record)
		db.session.commit()

	def last_added(value):

		record = event_information.query.filter(
			event_information.organizer_id==value
			).order_by(event_information.id.desc()
			).first()

		return record

	def retrieve_event(value):

		record = event_information.query.filter(event_information.id==value).first()

		return record

	def select_list():

		record = event_information.query.filter(event_information.event_status=='S').all()

		return record

	def calendar():

		record = event_information.query.filter(or_(
			event_information.event_status=='S', 
			event_information.event_status=='F')).all()

		return record

	def update_status(id, status):

		event = event_information.query.filter(event_information.id==id).first()
		event.event_status = status
		db.session.commit()		

	def reschedule(value):

		record = event_information.query.filter_by(id=value).first()

		return record

	def thrusts():

		record = event_information.query.add_columns(
			event_information.thrust,
			func.COUNT(event_information.thrust).label('count')
			).group_by(event_information.thrust
			).all()

		return record

	def status():

		record = event_information.query.add_columns(
			event_information.status,
			func.COUNT(event_information.id).label('count')
			).group_by(event_information.status
			).all()

		return record

class event_participation(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT, db.ForeignKey('event_information.id'), nullable=False)
	participant_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable=False)
	rating = db.Column(db.INT, nullable=True)
	comment = db.Column(db.VARCHAR(140),nullable=False)
	is_target = db.Column(db.CHAR(1), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	def add(value):

		record = event_participation(
			id = value[0],
			event_id = value[1],
			participant_id = value[2],
			rating = None,
			comment = None,
			is_target = value[3],
			status = 'J')

		db.session.add(record)
		db.session.commit()

	def show_status(value):

		record = event_participation.query.filter(
			and_(event_participation.event_id==value[0],
			event_participation.participant_id==value[1])
			).first()

		return record

	def user_joined(value):

		record = event_participation.query.filter(
			and_(event_participation.participant_id==value,
			event_participation.status=='J')
			).all()

		return record

	def show_joined(value):

		record = event_participation.query.filter(
			and_(event_participation.event_id==value,
			event_participation.is_target!='Y',
			event_participation.status!='R')
			).count()

		return record

	def update(value):

		record = event_participation.query.filter(
			event_participation.event_id==value[0], 
			event_participation.participant_id==value[1]
			).first()

		record.status=value[2]

		db.session.commit()

	def evaluate(value):

		record = event_participation.query.filter(
			event_participation.event_id==value[0], 
			event_participation.participant_id==value[1]
			).first()

		record.rating=value[2]
		record.comment=value[3]

		db.session.commit()		

	def ratings(value):

		record = event_participation.query.add_columns(
			event_participation.rating,
			func.COUNT(event_participation.rating).label('count')
			).group_by(event_participation.rating
			).filter(event_participation.event_id==value
			).all()

		return record

	def average_rating(value):

		record = event_participation.query.add_columns(
			func.AVG(event_participation.rating).label('average')
			).filter(event_participation.event_id==value
			).first()

		return record

class event_photo(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT, db.ForeignKey('event_information.id'))
	photo = db.Column(db.VARCHAR(200), nullable=False)
	description = db.Column(db.VARCHAR(140))
	is_used = db.Column(db.CHAR(1), nullable=False)

	def add(value):

		record = event_photo(
			id = value[0],
			event_id = value[1],
			photo = value[2],
			description = value[3],
			is_used = value[4]
			)

		db.session.add(record)
		db.session.commit()

	def show(value):

		record = event_photo.query.filter(and_(
			event_photo.event_id==value,
			event_photo.is_used=='Y')
			).order_by(event_photo.id.desc()
			).all()

		return record

	def caption(value):

		record = event_photo.query.filter(event_photo.id==value[0]).first()

		record.description = value[1]

		db.session.commit()

	def delete(value):

		record = event_photo.query.filter(event_photo.id==value).first()

		record.is_used = 'N'

		db.session.commit()


class inventory(db.Model):

	id = db.Column(db.INT, primary_key=True)
	donation_id = db.Column(db.INT, db.ForeignKey('donation.id'))
	type_id = db.Column	(db.INT, db.ForeignKey('inventory_type.id'), nullable=False)
	in_stock = db.Column (db.INT, nullable=False)
	given = db.Column (db.INT, nullable=False)
	expired = db.Column (db.INT, nullable=False)

	def add(value):

		record = inventory(
			id = value[0],
			donation_id	=value[1],
			type_id=value[2],
			in_stock=value[3],
			given=value[4],
			expired=value[5])

		db.session.add(record)
		db.session.commit()

	def item_breakdown():

		record = inventory.query.order_by(
			inventory.in_stock.desc(), 
			inventory.donation_id.asc()
			).all()

		return record

	def get_info(value):

		record = inventory.query.filter(inventory.id==value[0]).first()

		return record

	def get_recop(value):

		record = inventory.query.filter(and_(inventory.type_id==value, inventory.donation_id==None)).first()

		return record

	def update_recop(value):

		record = inventory.query.filter(inventory.id==value[0]).first()

		record.in_stock=value[1]

		db.session.commit()

	def give(value):

		record = inventory.query.filter(inventory.id==value[0]).first()

		record.given = value[1]
		record.in_stock = value[2]

		db.session.commit()

	def dispose(value):

		record = inventory.query.filter(inventory.id==value[0]).first()

		record.expired= value[1]
		record.in_stock= value[2]

		db.session.commit()

	def status():

		record = inventory.query.add_columns(
			func.SUM(inventory.in_stock).label('in_stock'),
			func.SUM(inventory.given).label('given'),
			func.SUM(inventory.expired).label('expired')
			).all()

		return record	

	def type():

		record = inventory.query.add_columns(
			inventory.type_id,
			func.SUM(inventory.in_stock).label('in_stock'),
			func.SUM(inventory.given).label('given'),
			func.SUM(inventory.expired).label('expired')
			).group_by(inventory.type_id
			).all()

		return record	
class inventory_type(db.Model):

	id = db.Column(db.INT, primary_key=True)
	name = db.Column(db.VARCHAR(20), nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)	

	inventory_type_id = db.relationship('inventory', backref='inventory_type', lazy=True)

	def add(value):

		record = inventory_type(
			id = value[0],
			name = value[1],
			status = value[2])

		db.session.add(record)
		db.session.commit()

	def show_list():

		record = inventory_type.query.filter(inventory_type.status=='A').order_by(inventory_type.name.asc()).all()

		return record

	def last_added():

		record = inventory_type.query.count()

		return record

	def duplicate(value):

		record = inventory_type.query.filter(
				inventory_type.name.like('%'+value+'%')
				).first()

		return record

class proposal_tracker(db.Model):

	id = db.Column(db.INT, primary_key=True)
	event_id = db.Column(db.INT, db.ForeignKey('event_information.id'), nullable=False)
	proposed_on = db.Column	(db.DATETIME, nullable=False)
	recop_accepted = db.Column(db.DATETIME)
	acad_signed = db.Column(db.DATETIME)
	fmi_signed = db.Column(db.DATETIME)
	approved_on = db.Column(db.DATETIME)
	comment = db.Column(db.VARCHAR(20))
	status = db.Column(db.CHAR(1), nullable=False)	

	def add(value):

		record = proposal_tracker(
			id = value[0],
			event_id = value[1],
			proposed_on = datetime.now(),
			recop_accepted = None,
			acad_signed = None,
			fmi_signed = None,
			approved_on = None,
			comment = None,
			status = value[2])

		db.session.add(record)
		db.session.commit()

	def update_status(id, status):

		proposal = proposal_tracker.query.filter(proposal_tracker.event_id==id).first()

		proposal.status = status

		if status=='A':
			proposal.recop_accepted = datetime.now()
		elif status=='F':
			proposal.acad_signed = datetime.now()
		elif status=='P':
			proposal.fmi_signed = datetime.now()
		elif status=='S':
			proposal.approved_on = datetime.now()
		else:
			proposal.comment = 'Declined'

		db.session.commit()

class referral(db.Model):

	id = db.Column(db.INT, primary_key=True)
	referrer_id = db.Column(db.INT)
	name = db.Column(db.VARCHAR(50),nullable=False)
	email_address = db.Column(db.VARCHAR(30),nullable=False)
	type = db.Column(db.INT, nullable=False)
	status = db.Column(db.CHAR(1), nullable=False)

	def add(value):

		record = referral(
			id=value[0], 
			referrer_id=value[1],
			name=value[2],
			email_address=value[3],
			type=value[4],
			status=value[5]
			)
			 
		db.session.add(record)
		db.session.commit()


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

	def add(value):

		record = user_account(
			id=value[0], 
			info_id=value[1],
			username=value[2],
			password=bcrypt.generate_password_hash(value[3]).decode('utf-8'),
			email_address=value[4],
			type=value[5],
			last_active=value[6],
			status=value[7]
			)
			 
		db.session.add(record)
		db.session.commit()

	def retrieve_user(value):

		record = user_account.query.filter(user_account.info_id==value).first()

		return record

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

	def profile_acc_update(value):

		record = user_account.query.filter_by(id=value).first()

		return record

	def user_type():

		record = user_account.query.add_columns(
			user_account.type,
			func.COUNT(user_account.id).label('count')
			).group_by(user_account.type
			).filter(and_(user_account.type!=1, user_account.type!=5)
			).all()

		return record

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
	comm_id = db.relationship('community_info', foreign_keys=[community_info.community_id], backref='user_information_community', lazy=True)
	comm_info_id = db.relationship('community_member', foreign_keys=[community_member.community_id], backref='user_information_community', lazy=True)
	mem_info_id = db.relationship('community_member', foreign_keys=[community_member.member_id], backref='user_information_member', lazy=True)
	organizer_info_id = db.relationship('event_information', backref='user_information', lazy=True)
	photo_info_id = db.relationship('user_photo', backref='user_information', lazy=True)

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

	def reserve_id():

		record = user_information.query.count()

		return record


	def linkage_info(value):

		record = user_information.query.filter(user_information.id==value).first()

		return record

	def profile_info_update(value):

		record = user_information.query.filter_by(id=value).first()

		return record
		
	def retrieve_user(value):

		record = user_information.query.filter(user_information.id==value).first()

		return record

	def thrusts():

		record = user_information.query.add_columns(
			user_information.thrust,
			func.COUNT(user_information.thrust).label('count')
			).group_by(user_information.thrust
			).filter(user_information.thrust!=0
			).all()

		return record

class user_photo(db.Model):

	id = db.Column(db.INT, primary_key=True)
	user_id = db.Column(db.INT, db.ForeignKey('user_information.id'), nullable='False')
	path = db.Column(db.VARCHAR(200),nullable=False)

	def add(value):

		record = user_photo(
			id=value[0],
			user_id=value[1],
			path=value[2]
			)

		db.session.add(record)
		db.session.commit()

	def update(value):

		record = user_photo.query.filter_by(user_id=value[0]).first()

		record.path = value[1]

		db.session.commit()		
		
	def photo(value):

		record = user_photo.query.filter_by(user_id=value).first()

		return record

