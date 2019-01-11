from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy 

bcrypt = Bcrypt()
login = LoginManager()
db = SQLAlchemy()