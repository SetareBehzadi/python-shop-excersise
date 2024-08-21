from celery import shared_task
from datetime import timedelta, datetime
from accounts.models import OtpCode
from zoneinfo import ZoneInfo


@shared_task
def clear_expired_otp():
    exp_time = datetime.now(tz=ZoneInfo("Asia/Tehran")) - timedelta(minutes=2)
    OtpCode.objects.filter(created_at__lt=exp_time).delete()
