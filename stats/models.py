from django.db import models
from core.models import CustomUser

class WaterWell(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    capacity = models.FloatField()  # in m³/h
    current_month_usage = models.FloatField(default=0.0)  # in m³
    current_kwh_consumption = models.FloatField(default=0.0)  # in kWh
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(CustomUser, related_name='water_wells')

    def __str__(self):
        return self.name

class WaterWellUsage(models.Model):
    water_well = models.ForeignKey(WaterWell, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    water_usage = models.FloatField()
    kwh_consumption = models.FloatField()  # in kWh
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.water_well.name} - {self.date}: {self.water_usage} m³/h, {self.kwh_consumption} kWh"
    
    class Meta:
        ordering = ['-date']