from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    PENDING = 'pending'
    AWAITING_APPROVAL = 'awaiting_approval'
    PAID = 'paid'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (AWAITING_APPROVAL, 'Awaiting Approval'),
        (PAID, 'Paid'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')} - {self.status}"

    # Helper method to check if payment is approved
    def is_approved(self):
        return self.status == self.PAID
    
