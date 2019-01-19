
class Config(object):
	
	SECRET_KEY = 'random_string'
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/recop-comex'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT= 465
	MAIL_USE_SSL=True
	MAIL_USERNAME = "recop.baste@gmail.com"
	MAIL_PASSWORD = "recopcomex"