from flask import url_for, redirect
from flask_login import current_user

def authenticate():
	
	if current_user.is_authenticated and not current_user.is_anonymous:

		if current_user.type == 2:
			return redirect(url_for('linkages.index'))

	return None