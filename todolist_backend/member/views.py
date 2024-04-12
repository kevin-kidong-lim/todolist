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
from .serializers import MemberSerializer,RegisterSerializer,MemberUpdateSerializer,MyTokenObtainPairSerializer
# Task model
from .models import Member
from .forms import RegisterForm, LoginForm
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import mixins
from rest_framework import generics
from django.conf import settings
from rest_framework import viewsets
from django.db import IntegrityError
from django.core import serializers
# from django.contrib.auth.models import User
from rest_framework import generics,status
from rest_framework.response import Response 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError, ParseError
from django.db.models import Q
from argon2 import PasswordHasher, exceptions 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
import json 

class RegisterView(generics.CreateAPIView): 
    queryset = Member.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        user_info = []
        serializer_class = super().create(request, *args, **kwargs)
    
        return Response({
            'status': 200,
            'message': 'ok',
            'data': serializer_class.data['user_id']
        })
    
class DtailView(generics.RetrieveUpdateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberUpdateSerializer
    
    def get_queryset(self):
        return super().get_queryset() 
    def put(self, request, *args, **kwargs):
        user_id = request.data['user_id']
        
        user_info = []
        try:
            user_info = Member.objects.filter(user_id=user_id)
        except ObjectDoesNotExist:
            print(' doesnt exist.')

        return self.update(request, *args, **kwargs)
    
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data 
        # return data
        return Response(data, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView, mixins.ListModelMixin):
    
  def post(self, request):
      res = Response({'message': 'Success Logout'}, status=status.HTTP_202_ACCEPTED)
      refresh_token = request.COOKIES.get('refreshtoken')
      token = RefreshToken(refresh_token)
      token.blacklist()
      res.delete_cookie('refreshtoken', httponly=True)
      return res