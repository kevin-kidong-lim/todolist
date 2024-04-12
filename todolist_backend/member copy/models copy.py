from django.db import models

# Create your models here.
class Member(models.Model):

    flag1 = '1'
    flag2 = '2'

    STATUS_CHOICES = (  
        (flag1, '일반 회원'),
        (flag2, '경매 회원')
    )

    user_id =  models.CharField(max_length=20,primary_key=True, unique=True,verbose_name='회원ID')
    user_nm =  models.CharField( max_length=20,verbose_name='이름')
    passwd =  models.CharField(max_length=128,verbose_name='비밀번호')
    email =  models.EmailField(max_length=128,unique=True,verbose_name='Email')
    post_cd =  models.CharField( max_length=10,verbose_name='우편번호')
    address =  models.CharField( max_length=200,verbose_name='주소1')
    address2 =  models.CharField(max_length=200,verbose_name='주소2')
    status =  models.CharField( max_length=8,verbose_name='회원상태')
    join_dt =  models.DateTimeField(auto_now_add=True,verbose_name='가입일')
    update_dt =  models.DateTimeField(auto_now_add=True,verbose_name='수정일')
    ip_address =  models.GenericIPAddressField( verbose_name='Ip주소')

    member_flag = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default=flag1 verbose_name='회원구분')  

    def __str__(self):
        return self.user_id
    

