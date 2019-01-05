from data_access.models import user

def query_sample():
	query = user.query.filter_by(id = 1).first()
	result = query.password
	return result