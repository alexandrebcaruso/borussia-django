from django import forms
from .models import Payment

class PaymentReceiptForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['receipt']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['receipt'].required = True
