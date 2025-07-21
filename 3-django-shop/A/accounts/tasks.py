from celery import shared_task
from utils import send_otp_code

@shared_task
def send_otp_code_task(phone, random_code):
    send_otp_code(phone, random_code)
