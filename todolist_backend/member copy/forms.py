from django import forms 
from .models import Member
from argon2 import PasswordHasher, exceptions 

class LoginForm(forms.Form):
    user_id =  forms.CharField(
        max_length= 20,
        label = '사용자ID',
        required=True,
        widget=forms.TextInput(
            attrs={
            'class' : 'user-id',
            'placeholder' :'사용자ID'
            }
        ),
        error_messages={'required':'사용자ID를 입력해주세요'}
    )
    passwd = forms.CharField(
        max_length= 128,
        label = '비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
            'class' : 'passwd',
            'placeholder' :'비밀번호'
            }
        ),
        error_messages={'required':'비밀번호를  입력해주세요'}
    )
    field_order = [
        'user_id',
        'passwd'
    ]

    def clean(self):
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id','')
        passwd = cleaned_data.get('passwd','')

        if user_id == '':
            return self.add_error('user_id','아이디를 다시 입력해주세요')
        elif passwd == '':
            return self.add_error('passwd','비밀번호를 다시 입력해주세요')
        else:
            try:
                user = Member.objects.get(user_id = user_id)
            except Member.DoesNotExist:
                return self.add_error('user_id','아이디가 존재하지 않습니다.')
            
            try:
                PasswordHasher().verify(user.passwd, passwd)
            except exceptions.VerifyMismatchError:
                return self.add_error('passwd','비밀번호가 다릅니다.')

            self.login_session = user.user_id




class RegisterForm(forms.ModelForm):
    user_id = forms.CharField(
        label = '사용자ID',
        required=True,
        widget=forms.TextInput(
            attrs={
            'class' : 'user-id',
            'placeholder' :'사용자ID'
            }
        ),
        error_messages={'required':'사용자ID를 입력해주세요'}
    )
    passwd = forms.CharField(
        label = '비밀번호',
        required=True,
        widget=forms.PasswordInput(
            attrs={
            'class' : 'passwd',
            'placeholder' :'비밀번호'
            }
        ),
        error_messages={'required':'비밀번호를  입력해주세요'}
    )
    user_pw2 = forms.CharField(
        label = '비밀번호 확인',
        required=True,
        widget=forms.PasswordInput(
            attrs={
            'class' : 'user-pw2',
            'placeholder' :'비밀번호 확인'
            }
        ),
        error_messages={'required':'비밀번호 확인을  입력해주세요'}
    )
    user_nm = forms.CharField(
        label = '이름',
        required=True,
        widget=forms.TextInput(
            attrs={
            'class' : 'user_nm',
            'placeholder' :'이름'
            }
        ),
        error_messages={'required':'이름을  입력해주세요'}
    )
    email = forms.EmailField(
        label = 'Email',
        required=True,
        widget=forms.TextInput(
            attrs={
            'class' : 'email',
            'placeholder' :'Email'
            }
        ),
        error_messages={'required':'Email을  입력해주세요'}
    )
    
    field_order = [
        'user_id',
        'passwd',
        'user_pw2',
        'user_nm',
        'email',
     
    ]

    class Meta:
        model = Member
        fields = [
            'user_id',
            'passwd',
            'user_nm',
            'email',
           
            
        ]
    
    def clean(self):
        print(" ########## clean start ")
        cleaned_data = super().clean()
        user_id = cleaned_data.get('user_id','')
        passwd = cleaned_data.get('passwd','')
        user_pw2 = cleaned_data.get('user_pw2','')
        user_nm = cleaned_data.get('user_nm','')
        email = cleaned_data.get('email','')
    

        if passwd != user_pw2:
            return self.add_error('user_pw2','비밀번호가 달라요')
        elif not (4 <= len(user_id) <= 16):
            return self.add_error('user_id','아이디는 4~26자로 입력해주세요.')
        else:
            self.user_id = user_id
            self.passwd = PasswordHasher().hash(passwd)
            self.user_pw2 = user_pw2
            self.user_nm = user_nm
            self.email = email
        
        print(" ########## clean end ")
