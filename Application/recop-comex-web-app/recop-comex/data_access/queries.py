#Queries involving multiple tables goes here
from extensions import db
from sqlalchemy import and_
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

	def show_all():

		record = user_account.query.join(
			user_information
			).add_columns(
			user_information.id,
			user_information.company_name,
			user_information.address,
			user_account.email_address,
			user_account.status,
			).filter(user_account.type==3
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