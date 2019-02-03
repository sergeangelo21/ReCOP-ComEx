from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 
from flask_mail import Mail

import pdfkit

bcrypt = Bcrypt()
login = LoginManager()
db = SQLAlchemy()
mail = Mail()