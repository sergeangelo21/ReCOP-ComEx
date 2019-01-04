from models import user

def query_sample():
	query = user.query.filter_by(id = 1).first()
	result = query.username
	return result