from flask import Flask
from config import Config

from blueprints.admin import admin
from blueprints.linkages import linkages
from blueprints.communities import communities
from blueprints.registered import registered
from blueprints.religious_admin import religious_admin
from blueprints.unregistered import unregistered

from extensions import login, db, bcrypt, mail

def create_app():

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(Config)

	app.register_blueprint(admin)
	app.register_blueprint(linkages)
	app.register_blueprint(communities)
	app.register_blueprint(registered)
	app.register_blueprint(religious_admin)
	app.register_blueprint(unregistered)

	extensions(app)

	return app

def extensions(app):

	bcrypt.init_app(app)
	login.init_app(app)
	db.init_app(app)
	mail.init_app(app)

	return None

create_app().run(port=8000, debug=1)