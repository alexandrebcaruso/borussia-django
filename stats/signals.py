from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import CustomUser
from .models import WaterClock

@receiver(post_save, sender=CustomUser)
def create_water_clock(sender, instance, created, **kwargs):
    if created:
        WaterClock.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def save_water_clock(sender, instance, **kwargs):
    instance.waterclock.save()