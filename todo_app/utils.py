import jwt
from datetime import datetime, timedelta
from django.conf import settings
from .models import User

jwt_secret = settings.JWT_SECRET_KEY

def generate_jwt_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(days=30)
    }
    token = jwt.encode(payload, jwt_secret, algorithm='HS256')
    return token

def validate_jwt_token(api_key):
    try:
        payload = jwt.decode(api_key, jwt_secret, algorithms=["HS256"])
        client_id = payload['user_id']
        valid_user = True
        return valid_user, client_id

    except jwt.ExpiredSignatureError:
        return False, None
    except jwt.InvalidTokenError:
        return False, None

def is_email_unique(email):
    """
   Check if an email is unique
   An email is considered unique if it is not already in use by any user
   i.e. Freelancer, Client or Agency

   :param email: Email to be checked
   :return: True if the email is unique, False otherwise
   """
    try:
        email_exists = User.objects.filter(email=email).exists()
        return email_exists
    except Exception as e:
        print(e)
        return False
