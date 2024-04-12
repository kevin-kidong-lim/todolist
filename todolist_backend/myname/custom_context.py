from django.contrib import admin
from django.contrib.admin import ModelAdmin
from member.models import Member# Import your Member model
from datetime import date
# from django.utils import timezone
from django.db.models import Q
from datetime import datetime,timedelta
import pytz
winnipeg_timezone = pytz.timezone('America/Winnipeg')

from django.db.models import Count
from django.db.models.functions import ExtractWeekDay, ExtractWeek,TruncMonth


def custom_admin_context(request):
    # Add your custom context data here
    announcement_count = 1
    today = date.today()
    # seoul_now = timezone.localtime(timezone.now(), timezone=timezone.pytz.timezone('Asia/Seoul')).date()
    print('custom_admin_context ===================== today', today)
   
    # utc_now = datetime.utcnow()
    # dtime = utc_now.replace(tzinfo=pytz.utc).astimezone(winnipeg_timezone)
    # date_format = "%Y-%m-%d %H:%M:%S"
    # date_object = dtime.strftime(date_format)

    server_time = datetime.now()

    # Convert server time to the Seoul timezone
    s_tz = pytz.timezone('America/Winnipeg')
    sl_time = server_time.astimezone(s_tz)
    s_now = sl_time.date()

    flag_none = '1'
    flag_apply = '2'
    flag_approved = '3'

    users_signed_up_today = Member.objects.filter(join_dt__date=s_now).count()
    total_member = Member.objects.filter().count()
    applied_or_approved_count = Member.objects.filter().count()
    auction_count = 0

    today = date.today()
    current_week_number = today.isocalendar()[1]

    signups_by_day = Member.objects.filter(join_dt__week=current_week_number).annotate(
        day_of_week=ExtractWeekDay('join_dt')
    ).values('day_of_week').annotate(signup_count=Count('join_dt')).order_by('day_of_week')
    signups_by_day_dict = {item['day_of_week']: item['signup_count'] for item in signups_by_day}
    signups_list = [signups_by_day_dict.get(day, 0) for day in range(1, 8)]

    registration_day = Member.objects.annotate(
        registration_day=ExtractWeekDay('join_dt')
    ).values('registration_day').annotate(signup_count=Count('join_dt')).order_by('registration_day')
    registration_day_dict = {item['registration_day']: item['signup_count'] for item in registration_day}

    registration_day_list = [registration_day_dict.get(day, 0) for day in range(1, 8)]


    current_date = datetime.now()
   
    monthly_counts_list = []
  
    monthly_list = []
  
    custom_data = {
        'notice_count': announcement_count,  # A
        'users_signed_up_today': users_signed_up_today,
        'total_member': total_member,
        'applied_or_approved_count': applied_or_approved_count,
        'auction_count': auction_count,
        'signups_list': signups_list,
        'monthly_list': monthly_list,
    }
    return {'custom_data': custom_data}