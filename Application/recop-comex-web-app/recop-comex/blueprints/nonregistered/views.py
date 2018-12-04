from flask import Blueprint, render_template
import os

nonregistered = Blueprint('nonregistered', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@nonregistered.route('/')
def sample():

	return render_template('index.html')