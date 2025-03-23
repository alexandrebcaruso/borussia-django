from django.db import models
from core.models import CustomUser

class WaterWell(models.Model):
    public_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=255)
    uf = models.CharField(max_length=2, null=True)
    locality = models.CharField(max_length=255)
    nature = models.CharField(max_length=100, null=True, blank=True)  # Permite nulo
    ne = models.FloatField(null=True, blank=True)
    nd = models.FloatField(null=True, blank=True)
    flow_rate = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  # Permite nulo
    longitude = models.FloatField(null=True, blank=True)  # Permite nulo
    capacity = models.FloatField()
    current_month_usage = models.FloatField(default=0.0)
    current_kwh_consumption = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    users = models.ManyToManyField(CustomUser, related_name='water_wells')

    def __str__(self):
        return self.name

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