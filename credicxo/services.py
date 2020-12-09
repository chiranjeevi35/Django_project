import datetime
import jwt
from django.conf import settings
from .models import signup_info
from rest_framework import exceptions

def generate_jwttoken(email):
    #Generating JWT(Json WEB Token) using email and role
    email = email.lower()
    ownership = getownership(email)
    access_token_payload = {
        'email' : email,
        'ownership': ownership,
        'exp' : datetime.datetime.utcnow()+datetime.timedelta(days=0, minutes=30),
        'iat' : datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm = 'HS256').decode('utf-8')
    print(access_token)
    return access_token

def getownership(email):
    #Getting Role by Email
    user = signup_info.objects.get(email=str(email))
    return user.role

def validatejwttoken(request):
    #Validating JWT Token 
    print(request)
    authorization_header = request.headers.get('Authorization')
    print(authorization_header)
    try:
        access_token = authorization_header.split(' ') [1]
        print("access token :"+access_token)
        payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=['HS256'])
        print(payload)
        print(payload.get('username'))
    except jwt.ExpiredSignatureError:
        raise exceptions.Authenticationfailed('accesstoken expired')        
    except IndexError:
        raise exceptions.Authenticationfailed('token prefix missing')
    except jwt.DecodeError:
        raise exceptions.Authenticationfailed('Invalid signature')
    except Exception as e:
        print(e)
        raise exceptions.Authenticationfailed(str(e))
    return payload.get('email'),payload.get('ownership')

