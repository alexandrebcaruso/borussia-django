from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Payment(models.Model):
    AWAITING_PAYMENT = 'awaiting_payment'
    AWAITING_APPROVAL = 'awaiting_approval'
    PAID = 'paid'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (AWAITING_PAYMENT, 'Aguardando pagamento'),  # New status
        (AWAITING_APPROVAL, 'Aguardando aprovação'),
        (PAID, 'Pago'),
        (REJECTED, 'Negado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AWAITING_PAYMENT)  # Default status
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')} - {self.status}"
        
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
    
