from django.db import models
from core.models import CustomUser

class WaterWell(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.FloatField()  # in liters
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(CustomUser, related_name='water_wells')

    def __str__(self):
        return self.name