#Queries involving multiple tables goes here
from extensions import db
from data_access.models import user_account, user_information

def partner_view():

	record = user_information.query.join(user_account).add_columns(user_information.first_name,user_account.password).filter(user_information.id==user_account.info_id).first()
	return record