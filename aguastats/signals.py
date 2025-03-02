# aguastats/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import WaterClock

@receiver(post_save, sender=User)
def create_water_clock(sender, instance, created, **kwargs):
    if created:
        WaterClock.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_water_clock(sender, instance, **kwargs):
    instance.waterclock.save()