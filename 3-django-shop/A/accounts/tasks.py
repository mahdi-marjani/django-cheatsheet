from celery import shared_task
from utils import send_otp_code
from accounts.models import OtpCode
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_otp_code_task(phone, random_code):
    send_otp_code(phone, random_code)

@shared_task
def remove_expired_otps():
    expired_time = timezone.now() - timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()