from flask import Blueprint, render_template
import os

admin = Blueprint('admin', __name__, template_folder="templates")

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@admin.route('/admin')
def sample():

	return render_template('/admin/index.html', title="Admin")