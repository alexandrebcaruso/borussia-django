from django.db import models
from django.conf import settings

class WaterClock(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    current_usage = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - Current Usage: {self.current_usage} m³"
    
class UsageStatistic(models.Model):
    water_clock = models.ForeignKey(WaterClock, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    water_usage = models.FloatField()
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.water_clock.user.username} - {self.date}: {self.water_usage} m³"
    
    class Meta:
        ordering = ['-date']
