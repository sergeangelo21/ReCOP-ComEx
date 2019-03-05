from flask import Flask, current_app
#from make_celery import make_celery
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature	
from mimetypes import MimeTypes
from config import Config
from extensions import mail

#app = Flask(__name__)
#celery = make_celery(app)

def generate(email):

    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

def confirm(token):

    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    email = serializer.loads(
    	token, salt=Config.SECURITY_PASSWORD_SALT)
        	
    return email

def send_email(parts):

    msg = Message(html=parts[0], subject=parts[1], sender = ("ReCOP Director", parts[2]), recipients=[parts[3]])

    mimes = MimeTypes()

    if parts[4]:

        for attachment in parts[4]:

            with current_app.open_resource(attachment.path) as file:

                mime = mimes.guess_type(file.name)
                
                if attachment.type==1:
                    name='Budget Plan'
                elif attachment.type==2:
                    name='Programme'
                elif attachment.type==3:
                    name='Signed Request Letter'

                msg.attach(name, mime[0], file.read())

    mail.send(msg)