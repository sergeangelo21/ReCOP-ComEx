#Queries involving multiple tables goes here
from extensions import db
from data_access.models import *

def partners_view():

	record = user_account.query.join(
		user_information
		).add_columns(
		user_information.id,
		user_information.company_name,
		user_information.address,
		user_account.status,
		).filter(user_account.type==3
		).all()

	return record