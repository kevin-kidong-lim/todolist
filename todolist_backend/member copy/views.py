# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# API definition for task
from .serializers import MemberSerializer,RegisterSerializer,LoginSerializer,MemberUpdateSerializer,FindPasswordSerializer,MyTokenObtainPairSerializer
# Task model
from .models import Member

from .forms import RegisterForm, LoginForm
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404, redirect, render

from rest_framework import mixins
from rest_framework import generics
from django.conf import settings

# from django.contrib.auth.models import User
from rest_framework import generics,status

from rest_framework.response import Response # 사용자가 request를 하면 응답을 해줘야하기 때문에 Response 사용
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, ParseError
from django.db.models import Q
from argon2 import PasswordHasher, exceptions 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
import json 
#  회원가입
class RegisterView(generics.CreateAPIView): # generics에서 CreateAPIView 사용 구현
    print('registerView start')
    queryset = Member.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        print('RegisterView > create')
        print('aaaaaaaaaaaaa')
        
        print('data1', request.data)

        user_info = []
       
        serializer_class = super().create(request, *args, **kwargs)
    
        return Response({
            'status': 200,
            'message': 'ok',
            'data': serializer_class.data['user_id']
        })

from rest_framework import viewsets
from django.db import IntegrityError
from django.core import serializers
class DtailView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberUpdateSerializer
    
    def get_queryset(self):
        return super().get_queryset() 
    def put(self, request, *args, **kwargs):
        print("detail view put", request.data)
        user_id = request.data['user_id']
        
        user_info = []
        try:
            user_info = Member.objects.filter(user_id=user_id)
            print('try user_info', user_info)
            print('query', user_info.query)
        except ObjectDoesNotExist:
            print(' doesnt exist.')
        print('user_info>', user_info)

        return self.update(request, *args, **kwargs)
    
from django.contrib.auth.hashers import check_password

    
# 로그인// 시리얼라이저를 통과해 얻어온 토큰을 그대로 응답해주는 방식
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver



class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data  # validate()의 리턴값인 Token을 받아옴. 
        print('@@@ MyTokenObtainPairView > post > data >>', data)
        
        # return data
        return Response(data, status=status.HTTP_200_OK)


from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token


class LoginView(generics.GenericAPIView): # 모델에 영향을 주지 않기 때문에 기본 제네릭 사용
    permission_classes = (permissions.AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request): 
        print("LoginView 111111111111111111111111111111111111 post start")
        # print('LoginView request.data', request.data)
        # print('LoginView request.Meta', request.META)
        # print('LoginView request.user', request.user)
        # print('LoginView request.path', request.path ) # 또는 요청에 대한 추가 정보
        # print('LoginView request.Meta', request.META.get('HTTP_REFERER')  ) # Referer 정보 가져오기
        print("LoginView 222222222222222222222222222 post start")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # validate()의 리턴값인 Token을 받아옴. 
        print("LoginView 33333333333333333333333333333 post start")
        print('LoginView token', token)
        print("token.user_id", token['user_id'])
        print("LoginView 444444444444444444444444444444 post start")
        
       
        print('token ---------------->', token)
        print("LoginView 5555555555555555555555555555555555555555 post start")
       
        return Response({"token": token}, status=status.HTTP_200_OK)


from rest_framework_simplejwt.tokens import RefreshToken
class CustomToken(RefreshToken):
    def get_payload(self):
        # Call the parent method to get the default payload
        payload = super().get_payload()
        # Add custom data to the payload
        payload.update({'user_nm': self.user.username})
        return payload


class LogoutAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    
  def post(self, request):
      res = Response({'message': 'Success Logout'}, status=status.HTTP_202_ACCEPTED)
      refresh_token = request.COOKIES.get('refreshtoken')
      token = RefreshToken(refresh_token)
      token.blacklist()
      res.delete_cookie('refreshtoken', httponly=True)
      return res
   
class FindPasswordView(generics.GenericAPIView): # 모델에 영향을 주지 않기 때문에 기본 제네릭 사용
    serializer_class = FindPasswordSerializer
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data  # validate()의 리턴값인 Token을 받아옴.
        return Response({"token": token}, status=status.HTTP_200_OK)  
    #  def post(self, request):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     token = serializer.validated_data  # validate()의 리턴값인 Token을 받아옴.
    #     return Response({"token": token.key}, status=status.HTTP_200_OK)
    

    # data = {'user_id': 'ultrax00', 'email': 'peter@example.org'}
    # json_object = json.dumps(data, indent = 4) 
    # return JsonResponse(data, status=201, safe=False)

    
# class MemberList(generics.ListCreateAPIView):
#     print('>>>>>>>>>>44>>>>>>> get')
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer

# class MemberList(mixins.ListModelMixin,
#                   mixins.CreateModelMixin,
#                   generics.GenericAPIView):
#     queryset = Member.objects.all()
#     serializer_class = MemberSerializer

#     def get(self, request, *args, **kwargs):
#         print('>>>>>>>>>>>>>>>>> get')
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         print("req.data", request.data)
#         request.data['status']= 'active'
#         request.data['ip_address']= '201.122.222.111'
#         return self.create(request, *args, **kwargs)
    
class MemberList(APIView):
    def get(self, request, format=None):
        member_list = Member.objects.all()
        serializer = MemberSerializer(member_list, many=True)
        return Response(serializer.data)
     
    def post(self, request, format=None):
        print("request.data ", request.data)
        request.data['status']= 'active'
        request.data['ip_address']= '201.122.222.111'
        serializer = MemberSerializer(data=request.data)
         
        print("serializer ", serializer)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET','POST'])
def member_list(request):
    print(" call member")
    if(request.method == 'GET'):
        member_list = Member.objects.all()
        serializer = MemberSerializer(member_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif(request.method == 'POST'):
        # register_form = RegisterForm(request.POST)
        # user_nm = request.POST['email']
        data = JSONParser().parse(request)

        data['status']= 'active'
        data['ip_address']= '201.122.222.111'

        serializer = MemberSerializer(data=data)
        print('post start ..................... user_nm 1: ', serializer)
        print('post start ..................... user_nm 1: ', data['user_id'])
        print('post start ..................... user_nm 2: ', data)
        
        print(" call member .............. post ",serializer.is_valid())
        # member_list = Member.objects.all()
        # serializer = MemberSerializer(member_list, many=True) 
        if serializer.is_valid():
            serializer.save()
           
            return JsonResponse(serializer.data, status=201)
        # return JsonResponse(serializer.errors, status=400)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        member_list = Member.objects.all()
        serializer = MemberSerializer(member_list, many=True)
        return JsonResponse(serializer.data, safe=False)
    
@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def member_detail(request, user_id):
    print('member_detail')
    try:
        member_detail = Member.objects.get(pk=user_id)
    except Member.DoesNotExist:
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = MemberSerializer(member_detail)
        return Response(serializer.data)
    

def logout(request):
    request.session.flush()
    return redirect('/')

# Create your views here.
# @csrf_exempt
# def login(request):
#     print('login ...', request)
#     # data = {
#     #     "user_id": "ultrax00"
#     #     }
#     data = {'user_id': 'ultrax00', 'email': 'peter@example.org'}
#     json_object = json.dumps(data, indent = 4) 
#     return JsonResponse(data, status=201, safe=False)

from django.shortcuts import render
from datetime import date
def admin_index(request):
    print('------------------- admin_index')
    today = date.today()
    users_signed_up_today = Member.objects.filter(join_dt__date=today).count()
    return render(request, 'admin/index.html', {'users_signed_up_today': users_signed_up_today})