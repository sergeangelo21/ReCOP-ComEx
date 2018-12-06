from flask import Blueprint, render_template
import os

partners = Blueprint('partners', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@partners.route('/partners')
def sample():

	return render_template('/partners/index.html')