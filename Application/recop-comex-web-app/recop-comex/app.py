from flask import Flask
from config import Config
from extensions import db

from blueprints.admin import admin
from blueprints.linkages import linkages
from blueprints.beneficiaries import beneficiaries
from blueprints.registered import registered
from blueprints.unregistered import unregistered

def create_app():

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(Config)

	app.register_blueprint(admin)
	app.register_blueprint(linkages)
	app.register_blueprint(beneficiaries)
	app.register_blueprint(registered)
	app.register_blueprint(unregistered)

	extensions(app)

	return app

def extensions(app):

    db.init_app(app)

    return None

create_app().run(port=8000, debug=1)