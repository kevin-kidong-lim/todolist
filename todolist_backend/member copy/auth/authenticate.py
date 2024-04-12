import datetime, jwt

from django.conf import settings

        # token['email'] = user.email
        # token['user_nm'] = user.user_nm
        # token['user_id'] = user.user_id
        # token['user_flag'] = user.member_flag

def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(
            days=0, minutes=60
        ),
        'iat': datetime.datetime.utcnow(),
    }
    
    access_token = jwt.encode(
        access_token_payload,
        settings.SECRET_KEY, algorithm='HS256'
    ).decode('utf-8')
    
    return access_token
    
    
def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow(),
    }
    
    refresh_token = jwt.encode(
        refresh_token_payload,
        settings.REFRESH_TOKEN_SECRET, algorithm='HS256'
    ).decode('utf-8')
    
    return refresh_token


def jwt_login(response, user):
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    
    data = {
        'access_token': access_token,
    }
    
    response.data = data
    response.set_cookie(key="refreshtoken", value=refresh_token, httponly=True)
    
    return response