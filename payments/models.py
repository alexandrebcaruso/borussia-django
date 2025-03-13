import os
from django.conf import settings
from django.db import models

def user_receipts_path(instance, filename):
    """Generate a folder path for the user's receipts."""
    return f'receipts/userid_{instance.user.id}/{filename}'

class Payment(models.Model):
    AWAITING_PAYMENT = 'awaiting_payment'
    AWAITING_APPROVAL = 'awaiting_approval'
    PAID = 'paid'
    REJECTED = 'rejected'

    STATUS_CHOICES = [
        (AWAITING_PAYMENT, 'Aguardando pagamento'),
        (AWAITING_APPROVAL, 'Aguardando aprovação'),
        (PAID, 'Pago'),
        (REJECTED, 'Negado'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AWAITING_PAYMENT)
    receipt = models.FileField(upload_to=user_receipts_path, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def receipt_exists(self):
        """Check if the receipt file exists on the filesystem."""
        if self.receipt:
            return os.path.isfile(self.receipt.path)
        return False

    def save(self, *args, **kwargs):
        # If the receipt is missing, set the status to "awaiting_payment"
        if not self.receipt_exists():
            self.status = self.AWAITING_PAYMENT
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the receipt file when the payment is deleted
        if self.receipt:
            if os.path.isfile(self.receipt.path):
                os.remove(self.receipt.path)
        super().delete(*args, **kwargs)

    def receipt_exists(self):
        """Check if the receipt file exists on the filesystem."""
        if self.receipt:
            return os.path.isfile(self.receipt.path)
        return False
