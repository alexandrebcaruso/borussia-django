from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from payments.models import CustomUser
from stats.models import WaterClock

class Command(BaseCommand):

    help = 'Create WaterClock objects for existing users'

    def handle(self, *args, **options):
        for user in CustomUser.objects.all():
            if not WaterClock.objects.filter(user=user).exists():
                WaterClock.objects.create(user=user)
                self.stdout.write(self.style.SUCCESS(f'Successfully created WaterClock for user {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'WaterClock already exists for user {user.username}'))