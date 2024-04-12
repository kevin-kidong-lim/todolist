from django.contrib.auth.backends import BaseBackend
from argon2 import PasswordHasher, exceptions 
from django.contrib.auth.signals import user_logged_in

from django.dispatch import Signal
from .models import Member
from django.contrib.auth.models import User
class MemberAuthBackend(BaseBackend):
    def authenticate(self, request, user_id=None, password=None):
        print('=================> MemberAuthBackend START ')
        try:
            member = Member.objects.get(user_id=user_id)
            print('=================> MemberAuthBackend OK')
            if PasswordHasher().verify( member.password,  password):
                # user_logged_in.send(sender=Member, request=request, user=member)
               
                try:
                    user = User.objects.get(username=user_id)
                except User.DoesNotExist:
                    # Create a new user. There's no need to set a password
                    # because only the password from settings.py is checked.
                    user = User(username=user_id)
                    user.is_staff = False
                    user.is_superuser = False
                    user.first_name = member.user_nm
                    user.save()
               
                return user
        except Member.DoesNotExist:
            print('=================> MemberAuthBackend EXCEPT ')
            return None

    def get_user(self, user_id):
        try:
            return Member.objects.get(user_id=user_id)
            # return User.objects.get(pk=user_id)
        except Member.DoesNotExist:
            return None

from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
class MemberTokenAuthentication(TokenAuthentication):
    print('##################### MemberTokenAuthentication #############')
    def authenticate(self, request):
        print('##################### authenticate 1234567999 #000############')

        # Extract the token from the request headers
        auth = request.headers.get('Authorization')
        
        if auth is None or not auth.startswith('Bearer '):
            # If no or invalid Authorization header, return None
            return None

        token = auth[len('Bearer '):]  # Extract the token value

        try:
            # Validate the token by calling authenticate_credentials
            user, token = self.authenticate_credentials(token)
            return user, token

        except AuthenticationFailed as e:
            # Handle authentication failure
            raise e  # or handle the exception as needed
    def authenticate_credentials(self, key):
        print('##################### authenticate_credentials #############')
        print('##################### key #############',key)
        try:
            member = Member.objects.get(auth_token=key)

        except Member.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not member.is_active:
            raise AuthenticationFailed('Member inactive or deleted')

        return member, key