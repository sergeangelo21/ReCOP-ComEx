#Queries involving multiple tables goes here
from extensions import db
from sqlalchemy import and_, or_, func
from data_access.models import *


class user_views():

	def login_info(value):

		record = user_information.query.join(
			user_account).add_columns(
			user_information.first_name, 
			user_information.company_name,
			user_information.address, 
			user_account.id).filter(
			user_account.id==value).first()

		return record

	def profile_info(value):

		record = user_information.query.join(
				user_account
				).add_columns(
				user_information.first_name,
				user_information.middle_name,
				user_information.last_name,
				user_information.company_name,
				user_information.bio,
				user_information.gender,
				user_information.birthday,
				user_information.address,
				user_information.address,
				user_information.telephone,
				user_information.mobile_number,
				user_account.username,
				user_account.password,
				user_account.email_address
				).filter(user_information.id==value).first()

		return record

	def signatory_info(value):

		record = user_information.query.join(
				user_account
				).add_columns(
				user_account.id,
				user_account.email_address,
				user_information.last_name
				).filter(user_account.id==value).first()

		return record

	def profile_info_update(value):

		record = user_information.query.filter_by(id=current_user.id).first()

		return record

	def profile_acc_update(value):

		record = user_account.query.filter_by(id=current_user.id).first()

		return record


class linkage_views():

	def show_list(value, type, search):

		if value=='all' and search==' ' :
			record = user_account.query.join(
				user_information
				).add_columns(
				user_account.id,
				user_account.info_id,
				user_information.company_name,
				(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name).label('coordinator'),
				user_information.partner_thrust,
				user_information.address,
				user_information.telephone,
				user_information.mobile_number,
				user_account.status
				).filter(user_account.type==type
				).order_by(user_account.info_id.asc()
				).all()
		elif value=='all' and search!=' ' :
			record = user_account.query.join(
				user_information
				).add_columns(
				user_account.id,
				user_account.info_id,
				user_information.company_name,
				(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name).label('coordinator'),
				user_information.partner_thrust,
				user_information.address,
				user_information.telephone,
				user_information.mobile_number,
				user_account.status
				).filter(and_(user_account.type==type,
				or_(user_information.company_name.like('%'+search+'%'),
				user_information.address.like('%'+search+'%'),
				user_information.first_name.like('%'+search+'%'),
				user_information.last_name.like('%'+search+'%')))
				).order_by(user_account.info_id.asc()
				).all()
		elif search!=' ':
			record = user_account.query.join(
				user_information
				).add_columns(
				user_account.id,
				user_account.info_id,
				user_information.company_name,
				(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name).label('coordinator'),
				user_information.partner_thrust,
				user_information.address,
				user_information.telephone,
				user_information.mobile_number,
				user_account.status,
				).filter(and_(user_account.type==type,user_account.status==value,
				or_(user_information.company_name.like('%'+search+'%'),
				user_information.address.like('%'+search+'%'),
				user_information.first_name.like('%'+search+'%'),
				user_information.last_name.like('%'+search+'%')))
				).order_by(user_account.info_id.asc()
				).all()	
		else:
			record = user_account.query.join(
				user_information
				).add_columns(
				user_account.id,
				user_account.info_id,
				user_information.company_name,
				(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name).label('coordinator'),
				user_information.partner_thrust,
				user_information.bio,
				user_information.address,
				user_information.telephone,
				user_information.mobile_number,
				user_account.status,
				).filter(and_(user_account.type==type, 
				user_account.status==value)
				).order_by(user_account.info_id.asc()
				).all()			

		return record

	def show_info(value):
		
		record = user_account.query.join(
			user_information
			).add_columns(
			user_account.id,
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
			).filter(user_account.info_id==value[0]
			).first()

		membership = audit_trail.query.filter(
			and_(audit_trail.affected_id==record.id, 
				audit_trail.target==value[1], 
				audit_trail.type==2)).first()


		return record, membership


	def target_linkages():

		record = user_information.query.join(
				user_account).add_columns(
				user_information.id, user_account.type, 
				user_information.address, user_information.company_name).filter(or_(
				user_account.type==4, user_account.type==3)).order_by(
				user_information.address.asc()
				).all()

		return record

class event_views():

	def show_list(value,search):

		if value=='all' and search==' ':
			record = event_information.query.join(
				user_information, proposal_tracker
				).add_columns(
				user_information.company_name,
				user_information.address,
				event_information.id,
				event_information.name,
				event_information.description,
				event_information.objective,
				event_information.location,
				event_information.event_date,
				event_information.min_age,
				event_information.max_age,
				event_information.thrust,
				event_information.type,
				event_information.event_status,
				proposal_tracker.proposed_on,
				proposal_tracker.status
				).order_by(proposal_tracker.proposed_on.desc()
				).all()

		elif value=='all' and search!=' ':
			record = event_information.query.join(
				user_information, proposal_tracker
				).add_columns(
				user_information.company_name,
				user_information.address,
				event_information.id,
				event_information.name,
				event_information.description,
				event_information.objective,
				event_information.location,
				event_information.event_date,
				event_information.min_age,
				event_information.max_age,
				event_information.thrust,
				event_information.type,
				event_information.event_status,
				proposal_tracker.proposed_on,
				proposal_tracker.status
				).filter(or_(user_information.company_name.like('%'+search+'%'),
				event_information.name.like('%'+search+'%'))
				).order_by(proposal_tracker.proposed_on.desc()
				).all()

		elif search!=' ':
			record = event_information.query.join(
				user_information, proposal_tracker
				).add_columns(
				user_information.company_name,
				user_information.address,
				event_information.id,
				event_information.name,
				event_information.description,
				event_information.objective,
				event_information.location,
				event_information.event_date,
				event_information.min_age,
				event_information.max_age,
				event_information.thrust,
				event_information.type,
				event_information.event_status,
				proposal_tracker.proposed_on,
				proposal_tracker.status
				).filter(and_(event_information.event_status==value,or_(
				user_information.company_name.like('%'+search+'%'),
				event_information.name.like('%'+search+'%')))
				).order_by(proposal_tracker.proposed_on.desc()
				).all()
		else:
			record = event_information.query.join(
				user_information, proposal_tracker
				).add_columns(
				user_information.company_name,
				user_information.address,
				event_information.id,
				event_information.name,
				event_information.description,
				event_information.objective,
				event_information.location,
				event_information.event_date,
				event_information.min_age,
				event_information.max_age,
				event_information.thrust,
				event_information.type,
				event_information.event_status,
				proposal_tracker.proposed_on,
				proposal_tracker.status
				).filter(event_information.event_status==value
				).order_by(proposal_tracker.proposed_on.desc()
				).all()			


		return record

	def show_info(value):
		
		record = event_information.query.join(
			user_information, proposal_tracker
			).add_columns(
			event_information.id,
			event_information.organizer_id,
			user_information.company_name,
			user_information.first_name,
			user_information.last_name,
			event_information.name,
			event_information.description,
			event_information.objective,
			event_information.budget,
			event_information.location,
			event_information.event_date,
			event_information.thrust,
			event_information.event_status,
			event_information.participant_no,
			event_information.max_age,
			event_information.min_age,
			proposal_tracker.proposed_on,
			proposal_tracker.recop_accepted,
			proposal_tracker.fmi_signed,
			proposal_tracker.acad_signed,
			proposal_tracker.approved_on,
			proposal_tracker.status
			).filter(event_information.id==value
			).first()

		return record

	def show_participants(value):

		record = event_participation.query.join(
			 user_information
			).add_columns(
			event_participation.event_id,
			(user_information.last_name + ', ' +
			user_information.first_name + ' '+ 
			func.left(user_information.middle_name,1) + '. '
			).label('name'),
			event_participation.is_target
			).filter(
			event_participation.event_id==value
			).order_by(user_information.last_name.asc()).all()

		return record

	def community_events(value):

		record = event_participation.query.join(
			event_information, user_information
			).add_columns(
			event_information.id,
			event_information.organizer_id,
			event_information.name,
			event_information.description,
			event_information.objective,
			event_information.budget,
			event_information.location,
			event_information.event_date,
			event_information.thrust,
			event_information.event_status,
			event_participation.participant_id,
			user_information.company_name
			).filter(and_(event_participation.participant_id==value, 
			event_information.event_status=='S')
			).all()

		return record

	def events_organized(value):

		record = event_information.query.join(
			user_information, proposal_tracker
			).add_columns(
			user_information.company_name,
			user_information.address,
			event_information.id,
			event_information.name,
			event_information.description,
			event_information.objective,
			event_information.location,
			event_information.event_date,
			event_information.min_age,
			event_information.max_age,
			event_information.thrust,
			event_information.type,
			event_information.event_status,
			proposal_tracker.proposed_on,
			proposal_tracker.status
			).filter(event_information.organizer_id==value
			).order_by(proposal_tracker.proposed_on.desc()
			).all()

		return record

class community_views():

	def members_list(search):

		if search==' ' :
			record = community.query.join(
				user_information, 
				or_(
				community.member_id==user_information.id,
				community.community_id==user_information.id)
				).add_columns(
				func.IF(user_information.id!=current_user.info_id,(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name),'').label('member'),
				user_information.address,
				community.status,
				user_information.id
				).filter(community.community_id==current_user.info_id
				).order_by(user_information.id.asc()
				).all()
		else:
			record = community.query.join(
				user_information,
				or_(
				community.member_id==user_information.id,
				community.community_id==user_information.id)
				).add_columns(
				func.IF(user_information.id!=current_user.info_id,(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name),'').label('member'),
				user_information.address,
				community.status,
				user_information.id
				).filter(community.community_id==current_user.info_id
				).all()			

		return record

	def event_participants(value):

		sub1 = community.query.join(
				user_information,
				community.member_id==user_information.id
				).join(event_participation
				).add_columns(
				(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name).label('name'),
				user_information.id,
				event_participation.status.label('status'),
				func.IF(community.occupation==None,"Unemployed",community.occupation).label('occupation'),
				community.religion,
				user_information.birthday
				).filter(community.community_id==current_user.info_id, event_participation.event_id==value
				)

		sub2 = community.query.join(
				user_information,
				community.member_id==user_information.id
				).add_columns(
				(user_information.first_name + ' ' +
				func.left(user_information.middle_name,1) + '. ' +
				user_information.last_name).label('name'),
				user_information.id,
				community.status.label('status'),
				func.IF(community.occupation==None,"Unemployed",community.occupation).label('occupation'),
				community.religion,
				user_information.birthday
				).filter(community.community_id==current_user.info_id, community.status=='A')

		record = sub1.union(sub2).group_by(user_information.id).all()

		return record

class donation_views():

	def show_list(value, search):

		sub1 = donation.query.join(
			user_information, 
			donation.sponsee_id==user_information.id
			).add_columns(
			donation.id,
			user_information.address.label('sponsee'),
			user_information.company_name,
			donation.event_id,
			donation.sponsee_id,
			donation.sponsor_id,
			donation.status,
			donation.date_given,
			func.IF(donation.amount==0.00,'In kind',donation.amount).label('amount')
			).filter(donation.sponsee_id!=None)

		sub2 = donation.query.join(
			event_information).join(
			user_information, 
			donation.sponsor_id==user_information.id).add_columns(
			donation.id,
			event_information.name.label('sponsee'),
			user_information.company_name,
			donation.event_id,
			donation.sponsee_id,
			donation.sponsor_id,
			donation.status,
			donation.date_given,
			func.IF(donation.amount==0.00,'In kind',donation.amount).label('amount')
			).filter(donation.event_id!=None)

		if value=='all' and search==' ' :

			record = sub1.union(sub2).order_by(donation.id.asc()).all()	

		elif value=='all' and search!=' ' :

			record = sub1.union(sub2).filter(or_(
				event_information.name.like('%'+search+'%'),
				user_information.address.like('%'+search+'%'))
				).group_by(donation.id
				).order_by(donation.id.asc()).all()		

		elif search!=' ':

			record = sub1.union(sub2).filter(and_(
				donation.status==value,or_(
				event_information.name.like('%'+search+'%'),
				user_information.address.like('%'+search+'%')))
				).group_by(donation.id
				).order_by(donation.id.asc()).all()	

		else:

			record = sub1.union(sub2).filter(donation.status==value).order_by(donation.id.asc()).all()	

		return record

	def show_sponsors():

		record = donation.query.join(
			user_information, 
			donation.sponsor_id==user_information.id
			).add_columns(
			donation.id.label('did'),
			user_information.id.label('id'),
			donation.sponsor_id==user_information.id).add_columns(
			donation.id,
			(user_information.first_name + ' ' +
			func.left(user_information.middle_name,1) + '. ' +
			user_information.last_name).label('name'),
			user_information.company_name).all()

		return record

