from flask import Blueprint, render_template
import os

beneficiaries = Blueprint('beneficiaries', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@beneficiaries.route('/beneficiaries')
def sample():

	return render_template('/beneficiaries/index.html', title="Beneficiaries")