from flask import Flask,make_response, send_file
#from make_celery import make_celery
from config import Config
import pdfkit

#app = Flask(__name__)
#celery = make_celery(app)

#@celery.task()
def generate_pdf(template,filepath):

	pdfkit.from_string(template, filepath, configuration=Config.PDF_CONFIG)