#Queries involving multiple tables goes here
from extensions import db
from sqlalchemy import and_, or_
from data_access.models import *


class user_views():

	def login_info(value):

		record = user_information.query.join(
			user_account).add_columns(
			user_information.first_name, 
			user_information.company_name, user_account.id).filter(
			user_account.id==value).first()

		return record

class partner_views():

	def show_list(value, search):

		if value=='all' and search==' ' :
			record = user_account.query.join(
				user_information
				).add_columns(
				user_information.id,
				user_information.company_name,
				user_information.first_name,
				user_information.middle_name,
				user_information.last_name,
				user_information.address,
				user_account.status,
				).filter(user_account.type==3
				).order_by(user_information.id.asc()
				).all()
		elif value=='all' and search!=' ' :
			record = user_account.query.join(
				user_information
				).add_columns(
				user_information.id,
				user_information.company_name,
				user_information.first_name,
				user_information.middle_name,
				user_information.last_name,
				user_information.address,
				user_account.status,
				).filter(and_(user_account.type==3,
				or_(user_information.company_name.like('%'+search+'%'),
				user_information.address.like('%'+search+'%'),
				user_information.first_name.like('%'+search+'%'),
				user_information.middle_name.like('%'+search+'%'),
				user_information.last_name.like('%'+search+'%')))
				).order_by(user_information.id.asc()
				).all()
		elif search!=' ':
			record = user_account.query.join(
				user_information
				).add_columns(
				user_information.id,
				user_information.company_name,
				user_information.first_name,
				user_information.middle_name,
				user_information.last_name,
				user_information.address,
				user_account.status,
				).filter(and_(user_account.type==3,user_account.status==value,
				or_(user_information.company_name.like('%'+search+'%'),
				user_information.address.like('%'+search+'%'),
				user_information.first_name.like('%'+search+'%'),
				user_information.middle_name.like('%'+search+'%'),
				user_information.last_name.like('%'+search+'%')))
				).order_by(user_information.id.asc()
				).all()	
		else:
			record = user_account.query.join(
				user_information
				).add_columns(
				user_information.id,
				user_information.company_name,
				user_information.first_name,
				user_information.middle_name,
				user_information.last_name,
				user_information.address,
				user_account.status,
				).filter(and_(user_account.type==3, 
				user_account.status==value)
				).all()			

		return record

	def show_info(value):
		
		record = user_account.query.join(
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
			user_account.username,
			user_account.email_address,
			user_account.last_active,
			user_account.status,
			).filter(user_account.id==value
			).first()

		membership = audit_trail.query.filter(
			and_(audit_trail.affected_id==value, 
				audit_trail.target=='partner', 
				audit_trail.type==2)).first()


		return record, membership

class event_views():

	def show_all():

		record = event_information.query.join(
			user_information
			).add_columns(
			user_information.company_name,
			event_information.id,
			event_information.name,
			event_information.event_date,
			event_information.event_status
			).all()

		return record

	def show_info(value):
		
		record = event_information.query.join(
			user_information, proposal_tracker
			).add_columns(
			event_information.id,
			user_information.company_name,
			event_information.name,
			event_information.description,
			event_information.objective,
			event_information.budget,
			event_information.location,
			event_information.event_date,
			event_information.thrust,
			event_information.event_status,
			proposal_tracker.proposed_on,
			proposal_tracker.recop_accepted,
			proposal_tracker.fmi_signed,
			proposal_tracker.acad_signed,
			proposal_tracker.approved_on,
			proposal_tracker.status
			).filter(event_information.id==value
			).first()

		return record
