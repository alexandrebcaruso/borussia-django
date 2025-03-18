from django.db import models
from core.models import CustomUser
from dashboard.models import WaterWell

class WaterClock(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    water_well = models.ForeignKey(WaterWell, on_delete=models.SET_NULL, null=True, blank=True)
    current_usage = models.FloatField(default=0.0)  # in m³
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s WaterClock"

class UsageStatistic(models.Model):
    water_clock = models.ForeignKey(WaterClock, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    water_usage = models.FloatField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.water_clock.user.username} - {self.date}: {self.water_usage} m³"
    
    class Meta:
        ordering = ['-date']
