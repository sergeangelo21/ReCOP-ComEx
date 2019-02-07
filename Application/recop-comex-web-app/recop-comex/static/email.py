from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer, BadSignature	
from config import Config
from extensions import mail


def generate(email):

    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

def confirm(token):

    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    email = serializer.loads(
    	token, salt=Config.SECURITY_PASSWORD_SALT)
        	
    return email

def send_email(parts):

	msg = Message(html=parts[0],
		subject=parts[1],
		sender = ("ReCOP Director", parts[2]),
		recipients=[parts[3]])

	mail.send(msg)


def send_email_resetpassword(parts):

    msg = Message(html=parts[0],
        subject=parts[1],
        sender = ("ReCOP Director", parts[2]),
        recipients=[parts[3]])

    mail.send(msg)