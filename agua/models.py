from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Payment(models.Model):
    REJECTED = 'rejected'
    PAID = 'paid'
    AWAITING_APPROVAL = 'awaiting_approval'

    STATUS_CHOICES = [
        (REJECTED, 'Rejected'),
        (AWAITING_APPROVAL, 'Awaiting Approval'),
        (PAID, 'Paid'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AWAITING_APPROVAL)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')} - {self.status}"

    # Helper method to check if payment is approved
    def is_approved(self):
        return self.status == self.PAID
    
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    roles = models.ManyToManyField('Role', related_name='users')

    def __str__(self):
        return self.username

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
