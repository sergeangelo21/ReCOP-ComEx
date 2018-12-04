from flask import Flask

from blueprints.recop import recop
from blueprints.partners import partners
from blueprints.beneficiaries import beneficiaries
from blueprints.registered import registered
from blueprints.nonregistered import nonregistered

def create_app():

	app = Flask(__name__, instance_relative_config=True)
	app.register_blueprint(recop)
	app.register_blueprint(partners)
	app.register_blueprint(beneficiaries)
	app.register_blueprint(registered)
	app.register_blueprint(nonregistered)

	return app

create_app().run(port=8000, debug=1)