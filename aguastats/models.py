from django.db import models
from django.contrib.auth.models import User

class UsageStatistic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    water_usage = models.FloatField()
    location = models.CharField(max_length=100)
    # Add more fields as needed

    def __str__(self):
        return f"{self.user} - {self.date.strftime('%Y-%m-%d')}"

    class Meta:
        ordering = ['-date']