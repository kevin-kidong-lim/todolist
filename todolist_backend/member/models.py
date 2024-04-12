from django.db import models

# Create your models here.
from django.utils.deconstruct import deconstructible
from django.utils import timezone
import random
import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        # ext = filename.split('.')[-1]
        extension = "." + filename.split('.')[-1]
        # set filename as random string
        # filename = '{}.{}'.format(uuid4().hex, ext)
        filename = str(random.randint(10,99)) + str(random.randint(10,99)) + str(random.randint(10,99)) + str(random.randint(10,99))  + extension
        # return the whole path to the file
        print('pathandrename flename>', filename)
        return os.path.join(self.path, filename)
    
path_and_rename = PathAndRename("files/company")

class UserManager(BaseUserManager):    
   
   use_in_migrations = True    
   
   def create_user(self, user_id, email, user_nm, password):        
       
       if not user_id:            
           raise ValueError('must have user email')
       if not password:            
           raise ValueError('must have user password')

       user = self.model(            
           user_id= user_id, #self.normalize_email(email),   
           email=email,
        user_nm=user_nm,       
       )        
    #    user.set_passwd(passwd)   
       user.set_password(password)        
       user.save(using=self._db)        
       return user

   def create_superuser(self, user_id,  email, user_nm, password):        
   
       user = self.create_user(            
           user_id= user_id,
           email=email, user_nm=user_nm,
           password=password        
       )
       user.is_admin = True
       user.is_superuser = True
       user.save(using=self._db)
       return user 
   
# class Member(models.Model):
class Member(AbstractBaseUser, PermissionsMixin):
   
    objects = UserManager()
 
    user_id =  models.CharField(max_length=50,primary_key=True, unique=True,verbose_name='User ID')
    user_nm =  models.CharField( max_length=20,verbose_name='Name')
    # passwd =  models.CharField(max_length=128,verbose_name='비밀번호')
    email =  models.EmailField(max_length=128,unique=True,verbose_name='Email')

    join_dt =  models.DateTimeField(auto_now_add=True,verbose_name='join date')
    update_dt =  models.DateTimeField(auto_now_add=True,verbose_name='update date')
   
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False) 
    
    USERNAME_FIELD = 'user_id'    
    # PASSWORD_FIELD = 'passwd'   
    REQUIRED_FIELDS = ['email','user_nm']

    def __str__(self):
        return self.user_id

    @property
    def is_staff(self):
        return self.is_admin

class LoginHistory(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, verbose_name='Member ID')
    login_date = models.DateTimeField(auto_now_add=True, verbose_name='Login Date')
    ip_address = models.CharField(max_length=50, verbose_name='IP Address')
    device_info  = models.CharField(max_length=500, verbose_name='Device Information',null=True, blank=True)
    host = models.CharField(max_length=50, verbose_name='Http Host',null=True, blank=True)
    referer = models.CharField(max_length=50, verbose_name='Referer',null=True, blank=True)
    path = models.CharField(max_length=100, verbose_name='Path',null=True, blank=True)

    class Meta:
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'

    def __str__(self):
        return f'{self.member.user_id} - {self.login_date}'

    # Add any additional methods or logic as needed