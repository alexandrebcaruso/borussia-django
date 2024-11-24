from django import forms
from .models import Payment

class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['receipt']  # Only the 'receipt' field needs to be handled

    # Custom validation for the uploaded receipt (optional, e.g., check file extension)
    def clean_receipt(self):
        receipt = self.cleaned_data.get('receipt')
        if receipt:
            # Check the file extension (optional validation)
            if not receipt.name.endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Please upload a valid image file (jpg, jpeg, png).")
        return receipt
