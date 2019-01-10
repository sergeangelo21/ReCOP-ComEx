
class Config(object):
	SECRET_KEY = 'random_string'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/recop-comex'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True