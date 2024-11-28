from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

# Custom User Admin to restrict user creation to only admins
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

    # Restrict "add user" option to only superusers
    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser:
            # If the user is not a superuser, remove the "add user" action
            if 'add' in actions:
                del actions['add']
        return actions

# Unregister the default User model and register with custom admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

from .models import Payment
from django.utils.html import format_html

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'status', 'receipt', 'uploaded_at', 'approved_at', 'actions')
    list_filter = ('status', 'user', 'month')
    search_fields = ('user__username', 'month')

    # Adding custom actions
    def actions(self, obj):
        if obj.status == Payment.AWAITING_APPROVAL:
            return format_html(
                '<a class="button" href="{}">Approve Receipt</a>',
                admin.url_for('admin:approve_payment', payment_id=obj.id)
            )
        return '-'

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('approve_payment/<int:payment_id>/', self.admin_site.admin_view(self.approve_payment), name='approve_payment'),
        ]
        return custom_urls + urls

    def approve_payment(self, request, payment_id):
        # Get the payment
        payment = get_object_or_404(Payment, id=payment_id)

        # Update status to 'Paid' and set the approval date
        payment.status = Payment.PAID
        payment.approved_at = timezone.now()
        payment.save()

        # Show success message
        self.message_user(request, f"Receipt for {payment.user.username} in {payment.month.strftime('%B %Y')} has been approved.")

        return redirect('admin:payments_payment_changelist')

# Register the custom admin
admin.site.register(Payment, PaymentAdmin)
