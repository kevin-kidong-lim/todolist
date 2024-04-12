from rest_framework import serializers, routers, viewsets
from .models import Member

from django.contrib.auth.models import User 
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.validators import UniqueValidator 
from rest_framework.authtoken.models import Token 
from argon2 import PasswordHasher, exceptions 
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        print('111111134444444444444444444444444444443111111')
        db_table = ''
        model = Member
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Member'
       
        fields = '__all__'
# work
class MemberUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        db_table = ''
        model = Member
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Member'
        fields = [
            'user_nm',
            'email',
            'join_dt',
        ]
    def update(self, instance, validated_data):
        member = Member.objects.get(pk=instance)
        member.user_nm=validated_data['user_nm']
        member.email=validated_data['email']
        member.save()
        return member
    
# work
class RegisterSerializer(serializers.ModelSerializer): 
  
    user_id = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Member.objects.all())], 
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(write_only=True, required=False) 
    class Meta:
        model = Member
        fields = [
            'password2'
        ]
        fields = '__all__'

    def validate(self, data): 
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return data

    def create(self, validated_data): 
        member = Member.objects.create(
            user_id=validated_data['user_id'],
            user_nm=validated_data['user_nm'],
            email=validated_data['email'],
        )
        member.set_password(validated_data['password'])
        member.save()

        return member
    
# work
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {'message':'user_id or password is incorrect!',
                              'success': False,
                              'status' : 401}
    }
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_nm'] = user.user_nm
        token['user_id'] = user.user_id
        token['user_flag'] = '3'
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['user_id'] = self.user.user_id
        data['user_nm'] = self.user.user_nm
        data['user_flag'] = '3'
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        return data