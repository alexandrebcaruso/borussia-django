from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    status = models.CharField(max_length=20, choices=[('paid', 'Paid'), ('pending', 'Pending'), ('failed', 'Failed')], default='pending')
    receipt = models.ImageField(upload_to='receipts/', null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')} - {self.status}"

    class Meta:
        unique_together = ('user', 'month')
