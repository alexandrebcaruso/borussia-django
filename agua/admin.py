from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from agua.models import CustomUser, Role, Payment
from django.utils import timezone
from django.shortcuts import redirect
from django.urls import path

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('roles',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'roles'),
        }),
    )

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'month', 'status', 'uploaded_at', 'approved_at')
    list_filter = ('status', 'month')
    search_fields = ('user__username', 'user__email')
    actions = ['approve_payments', 'reject_payments']

    def approve_payments(self, request, queryset):
        queryset.update(status='paid', approved_at=timezone.now())

    def reject_payments(self, request, queryset):
        queryset.update(status='pending', approved_at=None)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('manage-payments/', self.admin_site.admin_view(self.manage_payments), name='manage_payments'),
        ]
        return custom_urls + urls

    def manage_payments(self, request):
        return redirect('manage_payments')

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name',)

from django.contrib import admin
from .models import CustomUser, Role
