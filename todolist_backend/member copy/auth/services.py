
import requests

from django.conf import settings
from django.core.exceptions import ValidationError
import os



def google_get_access_token(google_token_api, code):
    client_id =  os.environ.get("GOOGLE_CLIENT_ID")
    client_secret =  os.environ.get("GOOGLE_CLIENT_SECRET")
    print('client_id', client_id)
    print('client_secret', client_secret)
    code = code
    grant_type = 'authorization_code'
    redirection_uri = getattr(settings,'GOOGLE_REDIRECTION_URL')   #settings.BASE_BACKEND_URL + "/api/v1/auth/login/google/callback"
    state = "random_string"
    data = {
          "grant_type":grant_type,
          "client_id": client_id,
          "client_secret":client_secret,
          "redirect_uri": redirection_uri,
          "code": code,
          "state": state,
        }
    print('data', data)
    google_token_api += \
        f"?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type={grant_type}&redirect_uri={redirection_uri}&state={state}"
    print('google_token_ap', google_token_api)
    token_response = requests.post(google_token_api, data)
    print('token_response', token_response)
    
    if not token_response.ok:
        raise ValidationError('google_token is invalid')
    
    access_token = token_response.json().get('access_token')
    
    return access_token


def google_get_user_info(access_token):
    user_info_response = requests.get(
        getattr(settings,'GOOGLE_USER_INFO_URL'),
        params={
            'access_token': access_token
        }
    )

    if not user_info_response.ok:
        raise ValidationError('Failed to obtain user info from Google.')
    
    user_info = user_info_response.json()
    
    return user_info


def kakao_get_access_token(token_api, code):
    client_id = os.environ.get("KAKAO_CLIENT_ID")
  
    code = code
    grant_type = 'authorization_code'
    redirection_uri = getattr(settings,'KAKAO_REDIRECTION_URL')  #settings.BASE_BACKEND_URL + "/api/v1/auth/login/google/callback"
    state = "random_string"
    data = {
          "grant_type":grant_type,
          "client_id": client_id, # 카카오 디벨로퍼 페이지에서 받은 rest api key
          "redirect_uri": redirection_uri,
          "code": code,
        }
    
    token_response = requests.post(token_api, data)
    
    if not token_response.ok:
        raise ValidationError('kakao_token is invalid 1 ')
    
    access_token = token_response.json().get('access_token')
    if not access_token:
        raise ValidationError('kakao_token is invalid 2')
    
    return access_token


def kakao_get_user_info(access_token):
    # user_info_response = requests.get(
    #     "https://kapi.kakao.com/v2/user/me",
    #     params={
    #         'access_token': access_token
    #     }
    # )
    # print('user_info>>', user_info)
    # if not user_info_response.ok:
    #     raise ValidationError('Failed to obtain user info from Google.')
    
    # user_info = user_info_response.json().get('kakao_account')
    # print('user_info>>', user_info)

    headers = {"Authorization": f"Bearer ${access_token}"}
    user_info_response = requests.get( getattr(settings,'KAKAO_USER_INFO_URL'), headers=headers).json() # 받은 access token 으로 user 정보 요청
    print('user_info_response>>', user_info_response)
    # data = {'access_token': access_token, 'code': code}
    user_info = user_info_response.get('kakao_account').get('profile')
    user_id = user_info_response.get('id')
    print('user_info>>', user_info)
    return user_info,user_id


def naver_get_access_token(token_api, code):
    client_id = os.environ.get("NAVER_CLIENT_ID")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET")
   
  
    code = code
    grant_type = 'authorization_code'
    redirection_uri = getattr(settings,'NAVER_REDIRECTION_URL')  #settings.BASE_BACKEND_URL + "/api/v1/auth/login/google/callback"
    state = "random_string"
    data = {
          "grant_type":grant_type,
          "client_id": client_id,
          "client_secret": client_secret,
          "redirect_uri": redirection_uri,
          "code": code,
          "state": "MYNAME_AUCTION"
        }
    print("naver_get_access_token: token",token_api)
    print("naver_get_access_token: data",data)
    token_response = requests.post(token_api, data)
    print("naver_get_access_token: token_response",token_response)
    
    if not token_response.ok:
        raise ValidationError('NAVER_token is invalid 1 ')
    
    access_token = token_response.json().get('access_token')
    print("naver_get_access_token: access_token",access_token)
    if not access_token:
        raise ValidationError('NAVER_token is invalid 2')
    
    return access_token


def naver_get_user_info(access_token):

    headers = {"Authorization": f"Bearer ${access_token}"}
    print('naver_get_user_info headers:', headers)
    # user_info_response = requests.get( getattr(settings,'NAVER_USER_INFO_URL'), headers=headers).json() # 받은 access token 으로 user 정보 요청
    user_info_response = requests.get(
                "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )

    print('naver_get_user_info url:', getattr(settings,'NAVER_USER_INFO_URL'))
    print('user_info_response>>', user_info_response)
    # data = {'access_token': access_token, 'code': code}
    if user_info_response.status_code != 200:
            raise ValidationError('NAVER_user_infor response is invalid')

    user_info = user_info_response.json().get("response")
    email = user_info["email"]

    # user_info = user_info_response.get('naver_account').get('profile')
    # user_id = user_info.get('id')
    print('user_info>>', user_info)
    print('email>>', email)
    user_id = generate_unique_id(user_info.get('id'),'N') #generate_random_string()
    
    print('user_id>>', user_id)
    return user_info,user_id

def convert_emailToUserId(email, site):
  username, domain = email.split('@')
  converted_email = username + site
  return converted_email

import random
import string
def generate_random_string(length=10):
# 영어 대문자, 소문자를 포함하는 문자열
  characters_alpha = string.ascii_letters

  # 숫자를 포함하는 문자열
  characters_numeric = string.digits

  # 랜덤 문자열 생성
  random_string = ''.join(random.choice(characters_alpha) for i in range(2))
  random_string += ''.join(random.choice(characters_numeric) for i in range(length - 2))

  return random_string

import base64
from django.test import TestCase

# Create your tests here.
import hashlib

def generate_unique_id(id, site):
  if not isinstance(id, str):
      raise TypeError("Input string must be of type str.")

  # Encode the input string to bytes
  string_bytes = id.encode('utf-8')

  # Generate the hash using SHA-256
  hash_digest = hashlib.sha256(string_bytes).digest()

  # Encode the hash to base64 and truncate to 12 characters
  truncated_hash = base64.urlsafe_b64encode(hash_digest)[:8].decode('utf-8')
  truncated_hash = site+truncated_hash

  return truncated_hash