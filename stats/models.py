from django.db import models
from core.models import CustomUser

class WaterWell(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.FloatField()  # in m³/h
    current_usage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(CustomUser, related_name='water_wells')

    def __str__(self):
        return self.name

class WaterWellUsage(models.Model):
    water_well = models.ForeignKey(WaterWell, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    water_usage = models.FloatField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.water_well.name} - {self.date}: {self.water_usage} m³/h"
    
    class Meta:
        ordering = ['-date']