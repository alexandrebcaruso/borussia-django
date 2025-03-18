from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import CustomUser
from stats.models import WaterClock
from dashboard.models import WaterWell

class Command(BaseCommand):

    help = 'Create WaterClock objects for existing users and associate them with a water well'

    def handle(self, *args, **options):
        for user in CustomUser.objects.all():
            if not WaterClock.objects.filter(user=user).exists():
                water_well = WaterWell.objects.first()  # Assign the first water well by default
                WaterClock.objects.create(user=user, water_well=water_well)
                self.stdout.write(self.style.SUCCESS(f'Successfully created WaterClock for user {user.username}'))
            else:
                self.stdout.write(self.style.WARNING(f'WaterClock already exists for user {user.username}'))