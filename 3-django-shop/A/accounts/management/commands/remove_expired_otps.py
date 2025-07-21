from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "remove all expired otp codes"

    def handle(self, *args, **options):
        expired_time = timezone.now() - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write(
            self.style.SUCCESS('all expired otp codes removed.')
        )