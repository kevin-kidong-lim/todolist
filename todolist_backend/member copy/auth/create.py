from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model

from member.models import Member
import random

User = get_user_model()

@transaction.atomic
def social_user_create(user_id, join_site, password=None, **extra_fields):
    existing_users = Member.objects.filter(email=extra_fields['email'])
    username, domain = email=extra_fields['email'].split("@")
    # 숫자를 랜덤하게 생성합니다.
    random_number = random.randint(0, 9999)
    if existing_users.exists():
        email = f"{username}+{random_number}@{domain}"
    else:
        email = extra_fields['email']

    user = Member(user_id=user_id, email= email)
    
    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()
    user.join_site = join_site
    # user.full_clean()
    # user.save()
   
    try:
        try:
            user.user_nm = extra_fields['first_name']
          
        except:
            try:
                user.user_nm = extra_fields['name']
            except:
                pass
    except:
        pass
    
    user.save()
    
    return user


@transaction.atomic
def social_user_get_or_create(user_id, join_site, **extra_data):
    print('social_user_get_or_create : user_id', user_id)
    print('social_user_get_or_create : email',  extra_data['email'])
    member = Member.objects.filter(user_id=user_id).first()
    print('social_user_get_or_create : member',  member)
    if member:
        print(print('memer already in table : member',  member))
        return member, False
    
    return social_user_create(user_id=user_id, join_site=join_site, **extra_data), True