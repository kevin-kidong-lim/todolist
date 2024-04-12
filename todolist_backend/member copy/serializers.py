from rest_framework import serializers, routers, viewsets
from .models import Member

from django.contrib.auth.models import User # 장고의 User 모델 사용
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate # django의 기본 authenticate 함수이다. (우리가 설정한 DefaultAuthBackend인 TokenAuth 방식으로 유저를 인증해줌.)
from rest_framework import serializers
from rest_framework.validators import UniqueValidator # 이메일 중복 방지를 위한 검증 도구 사용
from rest_framework.authtoken.models import Token # Token 모델 사용
from argon2 import PasswordHasher, exceptions 
class MemberSerializer(serializers.ModelSerializer):
    
    class Meta:
        print('111111134444444444444444444444444444443111111')
        db_table = ''
        model = Member
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Member'
       
        fields = '__all__'

class MemberUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        print('111111134444444444444444444444444444443111111')
        db_table = ''
        model = Member
        managed = True
        verbose_name = 'Member'
        verbose_name_plural = 'Member'
        fields = [
            # 'user_id',
            'user_nm',
            'email',
          
         
         
            'join_dt',
        
          
        ]
    def update(self, instance, validated_data): # CREATE 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함.
        # validated_data['ip_address']= '232.122.222.111'
        member = Member.objects.get(pk=instance)

        print('@@@@@@@@@@@@@@ update @################',validated_data)
        member.user_nm=validated_data['user_nm']
        # password=validated_data['password']
        member.email=validated_data['email']
     
        member.save()
        return member
    
    def update_password(self, instance, validated_data): # CREATE 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함.
        # validated_data['ip_address']= '232.122.222.111'
        member = Member.objects.get(pk=instance)

        print('@@@@@@@@@@@@@@ update_password @################',validated_data)
        member.password=validated_data['p1']
        # password=validated_data['password']

        member.save()
        return member

class RegisterSerializer(serializers.ModelSerializer):  # 회원가입 시리얼라이저 
    print('1111111333333333333333333333333333111111')
    user_id = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Member.objects.all())], # id 대한 중복 검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password], # 비밀번호에 대한 검증
    )
    password2 = serializers.CharField(write_only=True, required=False) # 비밀번호 확인을 위한 필드
    print('1111111111111')


# from member.serializers import RegisterSerializer
# >>> serial = RegisterSerializer()  
# >>> print(repr(serial))

# from member.serializers import MemberSerializer

# >>> from member.serializers import MemberSerializer
# >>> serial = MemberSerializer()  
# >>> print(repr(serial))

    class Meta:
        print('111111133555555555555555555555555555555553333333333111111')
        model = Member
        fields = [
            'password2'
        ]
        fields = '__all__'

    def validate(self, data): # 추가적으로 비밀번호 일치여부를 판단함.
        print('2222222222222')
        print('password', data['password'])
        print('password2', data['password2'])

        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return data

    def create(self, validated_data): # CREATE 요청에 대해 create 메소드를 오버라이딩, 유저를 생성하고 토큰을 생성하게 함.
        # validated_data['ip_address']= '232.122.222.111'
        
        print('@@@@@@@@@@@@@@@ create ################',validated_data)
        
        member = Member.objects.create(
            user_id=validated_data['user_id'],
            user_nm=validated_data['user_nm'],
          
            email=validated_data['email'],
           
           
        )
        member.set_password(validated_data['password'])
        member.save()

        # member.set_password(validated_data['password'])
        
        # token = Token.objects.create(user=member)
        
        return member
    

from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
class LoginSerializer(serializers.Serializer): # 로그인을 위한 시리얼라이저
    user_id = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    # write_only 옵션을 통해 클라이언트 -> 서버 방향의 역직렬화 가능. 서버-> 클라이언트의 직렬화는 불가
    print('LoginSerializer > user_id', user_id)
    print('LoginSerializer > password', password)

    def validate(self, data):
        # member = authenticate(**data)
        print('LoginSerializer > validate > user_id:', data['user_id'])
        user_id = data['user_id']
        try:
            member = Member.objects.get(user_id = user_id)
            # member = authenticate(**data)
            # token = Token.objects.get(user=member) # 토큰에서 유저를 찾아서 응답하는 코드
            print('member user_id', member.user_id)
            print('member password:', member.password)
            print('post password ', data['password'])
            print('hashed password ', PasswordHasher().hash( data['password']) )
            try:
                
                password_matches = check_password(data['password'], member.password)
                if password_matches:
                        print('Password is correct')
                else:
                    print('Password is incorrect')
                # if PasswordHasher().verify( member.password,  data['password']):
                if check_password(data['password'], member.password):

                    # try:
                    #     user = User.objects.get(username = user_id)
                    # except User.DoesNotExist:
                    #     # Create a new user. There's no need to set a password
                    #     # because only the password from settings.py is checked.
                    #     user = User(username = user_id)
                    #     user.is_staff = False
                    #     user.is_superuser = False
                    #     user.first_name = member.user_nm
                    #     user.save()
                    token2, created = Token.objects.get_or_create(user=member)

                    refresh = RefreshToken.for_user(user=member)
                    token = {
                        'user_id': member.user_id,
                        'user_nm': member.user_nm,
                        'user_flag':'3',
                        'token': token2.key,
                        'refresh': str(refresh),
                        'access':str(refresh.access_token),
                    }
                else:
                    token = {
                        'user_id': '', #member.user_id,
                        'user_nm': '', #member.user_nm
                        'user_flag': ''
                    }
            except exceptions.VerifyMismatchError:
                token = {
                        'user_id': '', #member.user_id,
                        'user_nm': '', #member.user_nm
                        'user_flag': ''
                    }
           
            return token
        except Member.DoesNotExist:
            token = {
                'user_id': '', #member.user_id,
                'user_nm': 'DoesNotExist' #member.user_nm
            }
            return token
        #     raise serializers.ValidationError(
        #     {"error": "등록된 사용자가 아닙니다."})

        # raise serializers.ValidationError(
        #     {"error": "등록된 사용자가 아닙니다."})

class FindPasswordSerializer(serializers.Serializer): # 로그인을 위한 시리얼라이저
    user_id = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    # password = serializers.CharField(required=True, write_only=True)
    # write_only 옵션을 통해 클라이언트 -> 서버 방향의 역직렬화 가능. 서버-> 클라이언트의 직렬화는 불가
    # print('FindPasswordSerializer > user_id', user_id)
    print('FindPasswordSerializer > email', email)

    def validate(self, data):
        # member = authenticate(**data)
        # print(data['user_id'])
        try:
            member = Member.objects.get(email=data['email'])
            # member = authenticate(**data)
            # token = Token.objects.get(user=member) # 토큰에서 유저를 찾아서 응답하는 코드
            print('member user_id', member.user_id)
            print('member password', member.password)


            token = {
                'user_id': member.user_id,
                'user_nm': member.user_nm,
                'user_flag': '3',
                'email': member.email
            }
        
            return token
        except Member.DoesNotExist:
            token = {
                'user_id': '', #member.user_id,
                'user_nm': 'DoesNotExist', #member.user_nm
                'user_flag': '',
                'email': ''
            }
            return token
        

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        
         # response에 추가하고 싶은 key값들 추가
        data['user_id'] = self.user.user_id
        data['user_nm'] = self.user.user_nm
        data['user_flag'] = '3'
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['success'] = True
        
        # 추가적인 처리가 필요한 경우 여기에 작성한다
        print('@@@@@@@ MyTokenObtainPairSerializer ====>')

        return data