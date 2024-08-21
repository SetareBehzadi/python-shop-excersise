from django.core.management.base import BaseCommand, CommandError
from datetime import timedelta, datetime
from accounts.models import OtpCode
from zoneinfo import ZoneInfo


class Command(BaseCommand):
    help = 'remove expired otpCode that created_at is greater than minutes'

    def handle(self, *args, **options):
        exp_time = datetime.now(tz=ZoneInfo("Asia/Tehran")) - timedelta(minutes=5)
        OtpCode.objects.filter(created_at__lt=exp_time).delete()
        self.stdout.write(
            self.style.SUCCESS('Successfully remove otpCode!')
        )
