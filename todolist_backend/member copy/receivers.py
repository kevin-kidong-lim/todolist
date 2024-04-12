
from django.apps import apps
from django.dispatch import receiver

from django.utils import timezone
from django.shortcuts import get_object_or_404
from .signals import user_logged_in_signal, user_actions_in_signal
@receiver(user_logged_in_signal)
def on_user_logged_in(sender, request, user, **kwargs):
    # Perform actions when the custom signal is received (user logged in)
    LoginHistory = apps.get_model('member', 'LoginHistory')
    Member = apps.get_model('member', 'Member')
    print('on_user_logged_in  reciver ....')
    ip_address = request.META.get('REMOTE_ADDR')
    device_info = request.META.get('HTTP_USER_AGENT')
    referer = request.META.get('HTTP_REFERER')
    path = request.META.get('PATH_INFO')
    host = request.META.get('HTTP_HOST')
    member = get_object_or_404(Member, user_id = request.data['user_id'])
    # # Create LoginHistory entry
    LoginHistory.objects.create(member=member, login_date=timezone.now()
                                , ip_address=ip_address
                                , device_info=device_info
                                , path=path
                                , host=host
                                , referer=referer
                                 )
    
#     아이피 상세정보 얻기.
#     http://ip-api.com/json/24.77.21.48

# "status": "success",
# "country": "Canada",
# "countryCode": "CA",
# "region": "MB",
# "regionName": "Manitoba",
# "city": "Winnipeg",
# "zip": "R3Y",
# "lat": 49.7851,
# "lon": -97.2117,
# "timezone": "America/Winnipeg",
# "isp": "Shaw Communications Inc.",
# "org": "Shaw Communications Inc.",
# "as": "AS6327 Shaw Communications Inc.",
# "query": "24.77.21.48"
# }import requests

# def get_country_region_from_ip(ip_address):
#     url = f"http://ip-api.com/json/{ip_address}"

#     try:
#         response = requests.get(url)
#         data = response.json()

#         country = data.get('country')
#         region = data.get('regionName')
        
#         return country, region
#     except requests.RequestException as e:
#         print(f"Request failed: {e}")
#         return None, None

# # Example usage:
# ip_address = '24.77.21.48'
# country, region = get_country_region_from_ip(ip_address)
# print(f"Country: {country}, Region: {region}")


from django.db.models.signals import post_save
from .models import LoginHistory
@receiver( post_save, sender = LoginHistory)
def localhistory_post_save( sender, **kwargs ):
    print('localhist post =============================>')
    histo = kwargs[ 'instance' ].member
    print('history>>>>>', histo)

@receiver( user_actions_in_signal)
def on_user_actions_in(sender, request, user, auction_no, **kwargs):
    print('user_actions_in_signal === on_user_actions_in')
    print('user_actions_in_signal === request ', request)
    print('user_actions_in_signal === auction_no ', auction_no)
    print('user_actions_in_signal === task ', kwargs.get('task'))
    print('user_actions_in_signal request.data', request.data)
    # print('user_actions_in_signal request.Meta', request.META)
    print('user_actions_in_signal request.user', request.user)
    print('user_actions_in_signal request.path', request.path ) # 또는 요청에 대한 추가 정보
    print('user_actions_in_signal request.Meta', request.META.get('HTTP_REFERER')  ) # Referer 정보 가져오기
# post_save.connect(localhistory_post_save, sender=LoginHistory)
# 경매 상세페이지 조회시 뷰 카운터 업데이트 하기 ..
# @receiver( post_save, sender = Pizzazip 
#           )def pizzazip_post_save( sender, **kwargs ):   
# location = kwargs[ 'instance' ].location   
# location.num_pizzazip += 1    
# location.save( )

# utils 로 옮기기 ..

# 사용자 액션 상태값 업데이트 ( 메뉴 클릭한것 보기 ..)