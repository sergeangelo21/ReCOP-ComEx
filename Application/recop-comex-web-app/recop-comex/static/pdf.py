from flask import make_response, send_file
from config import Config
import pdfkit

def generate_pdf(template,filepath):

	pdfkit.from_string(template, filepath, configuration=Config.PDF_CONFIG)