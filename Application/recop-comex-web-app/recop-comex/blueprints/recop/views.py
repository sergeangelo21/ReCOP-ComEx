from flask import Blueprint, render_template
import os

recop = Blueprint('recop', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@recop.route('/')
def sample():

	return render_template('index.html')