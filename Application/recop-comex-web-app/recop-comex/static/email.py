from itsdangerous import URLSafeTimedSerializer, BadSignature	
from config import Config


def generate(email):

    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    return serializer.dumps(email, salt=Config.SECURITY_PASSWORD_SALT)

def confirm(token, expiration=3600):

    serializer = URLSafeTimedSerializer(Config.SECRET_KEY)

    email = serializer.loads(
    	token, salt=Config.SECURITY_PASSWORD_SALT, max_age=expiration)

        	
    return email