from flask import Blueprint, render_template
import os

registered = Blueprint('registered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@registered.route('/registered')
def sample():

	return render_template('/registered/index.html')