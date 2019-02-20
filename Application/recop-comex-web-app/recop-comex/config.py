import pdfkit

class Config(object):
	
	SECRET_KEY = 'together_we_can'
	SECURITY_PASSWORD_SALT = "yes_we_can"

	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/recop-comex'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_ECHO = True

	MAIL_SERVER='smtp.gmail.com'
	MAIL_PORT= 465
	MAIL_USE_SSL=True
	MAIL_USERNAME = "recop.baste@gmail.com"
	MAIL_PASSWORD = "recopcomex"
	MAIL_ASCII_ATTACHMENTS = True 

	PDF_CONFIG = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
