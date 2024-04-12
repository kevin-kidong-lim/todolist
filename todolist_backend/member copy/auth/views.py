
from member.auth.services import google_get_access_token, google_get_user_info, \
                            kakao_get_access_token,kakao_get_user_info, \
                            naver_get_access_token,naver_get_user_info
from member.auth.authenticate import jwt_login
from member.auth.create import social_user_get_or_create
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import permissions
from member.serializers import MyTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
import os
class OAuth2NaverView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        print('@@@@@@@@@@@@@@@> OAuth2NaverView > code: ', code )
        access_token = naver_get_access_token( getattr(settings,'NAVER_ACCESS_TOKEN_OBTAIN_URL'), code)
        user_data , user_id = naver_get_user_info(access_token=access_token)
        print('@@@ user_data >', user_data)
        # user_info>> {'id': 'k1q0xBdnlygXqUi4p9_M_Lu6_VXCpmv7ac1f8KXBNUI',
        #               'email': 'ultrax00@naver.com', 'mobile': '431-999-7533', 
        #               'mobile_e164': '+824319997533', 'name': '임기동'}
        
        profile_data = {
            'email': user_data.get('email', ''),  #user_data.get('email', ''),
            'first_name': user_data.get('name', ''),
            'last_name': user_data.get('name', ''),
            'nickname': user_data.get('name', ''),
            'name': user_data.get('name', ''),
            'image': None,
            'path': "naver",
        }
        print('@@@@@@@@@@@@@@@@123 profile_data>',profile_data)
        # 회원가입_ 없으면 생성, 있으면 정보 가져오기.
        member, flg = social_user_get_or_create(str(user_id),'NAVER',**profile_data)
        print('@@@@@@@@@@@@@@@@ member>',member)
        print('@@@@@@@@@@@@@@@@ member user_nm >',member.user_nm)
        print('@@@@@@@@@@@@@@@@ flg>',flg)
        refresh = MyTokenObtainPairSerializer.get_token(member)
        data = {}
        data['user_id'] = member.user_id
        data['user_nm'] = member.user_nm
        data['user_flag'] = member.member_flag
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        print('@@@ data', data)



        response = Response(status=status.HTTP_302_FOUND)
       
        response['Location'] =  os.environ.get("FRONTEND_URL") + '?token=' + str(refresh.access_token) +'&refresh_token=' +str(refresh)
        return response       

class OAuth2KakaoView(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        print('@@@@@@@@@@@@@@@> OAuth2KakaoView > code: ', code )
        access_token = kakao_get_access_token( getattr(settings,'KAKAO_ACCESS_TOKEN_OBTAIN_URL'), code)
        user_data , user_id = kakao_get_user_info(access_token=access_token)
        print('@@@ user_data >', user_data)
        
        profile_data = {
            'email': str(user_id) + "@kakao.com",  #user_data.get('email', ''),
            'first_name': user_data.get('nickname', ''),
            'last_name': user_data.get('nickname', ''),
            'nickname': user_data.get('nickname', ''),
            'name': user_data.get('nickname', ''),
            'image': user_data.get('picture', None),
            'path': "kakao",
        }
        print('@@@@@@@@@@@@@@@@123 profile_data>',profile_data)
        # 회원가입_ 없으면 생성, 있으면 정보 가져오기.
        member, flg = social_user_get_or_create(str(user_id),'KAKAO',**profile_data)
        print('@@@@@@@@@@@@@@@@ member>',member)
        print('@@@@@@@@@@@@@@@@ member user_nm >',member.user_nm)
        print('@@@@@@@@@@@@@@@@ flg>',flg)
        refresh = MyTokenObtainPairSerializer.get_token(member)
        print('@@@@@@@@@@@@@@@@ refresh>',refresh)
        data = {}
        data['user_id'] = member.user_id
        data['user_nm'] = member.user_nm
        data['user_flag'] = member.member_flag
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        print('@@@ data', data)

        if member.user_id != '':       
            user_logged_in_signal.send(sender=self, request=request, user=member)

        response = Response(status=status.HTTP_302_FOUND)
        response.set_cookie(key="refreshtoken", value=refresh, httponly=True)
        response['Location'] = os.environ.get("FRONTEND_URL") + '?token=' + str(refresh.access_token) + '&refresh_token=' +str(refresh)+ '&user_nm=' + member.user_nm
        return response       

class OAuth2GoogleView(APIView):
    permission_classes = (permissions.AllowAny,) 

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        print('@@@@@@@@@@@@@@@> OAuth2GoogleView > code: ', code )
        google_token_api =  getattr(settings,'GOOGLE_ACCESS_TOKEN_OBTAIN_URL')
        print("google_token_api",google_token_api)
        access_token = google_get_access_token(google_token_api, code)
        user_data = google_get_user_info(access_token=access_token)
        print('@@@ user_data >', user_data)
        
        profile_data = {
            'email': user_data['email'],
            'first_name': user_data.get('given_name', ''),
            'last_name': user_data.get('family_name', ''),
            'nickname': user_data.get('nickname', ''),
            'name': user_data.get('name', ''),
            'image': user_data.get('picture', None),
            'path': "google",
        }
        print('@@@@@@@@@@@@@@@@123 profile_data>',profile_data)
        # 회원가입_ 없으면 생성, 있으면 정보 가져오기.
        member, flg = social_user_get_or_create(user_data.get('sub', '1'),'GOOGLE',**profile_data)
        print('@@@@@@@@@@@@@@@@ member>',member)
        print('@@@@@@@@@@@@@@@@ member user_nm >',member.user_nm)
        print('@@@@@@@@@@@@@@@@ flg>',flg)
        # user = authenticate(request, user_id=member.user_id, password=None)
        # print('@@@@@@@@@@@@@@@@ user>',user)
        # refresh = RefreshToken.for_user(member)
        refresh = MyTokenObtainPairSerializer.get_token(member)
        # token = CustomToken.for_user(refresh)
        # access_token = str(token.access_token)
        # access_token = str(refresh.access_token)
        print('@@@@@@@@@@@@@@@@ refresh>',refresh)
        # print('@@@@@@@@@@@@@@@@ access_token>',access_token)
        # 토큰생성_
        # settings.BASE_FRONTEND_URL
        
        # response = jwt_login(response=response, user=user)
        data = {}
        data['user_id'] = member.user_id
        data['user_nm'] = member.user_nm
        data['user_flag'] = member.member_flag
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        print('@@@ data', data)
        # response = redirect('http://localhost:8080/google-login')
        # response = HttpResponseRedirect('http://localhost:8080/google-login')
        # response.data = data
        # response.set_cookie(key="refreshtoken", value=refresh, httponly=True)
        # print('@@ response', response)
        # return response

        if member.user_id != '':       
            user_logged_in_signal.send(sender=self, request=request, user=member)
        response = Response(status=status.HTTP_302_FOUND)
        response.set_cookie(key="refreshtoken", value=refresh, httponly=True)
        response['Location'] =   os.environ.get("FRONTEND_URL")  + '?token=' + str(refresh.access_token) + '&refresh_token=' +str(refresh)+ '&user_nm=' + member.user_nm
        return response
    







































































