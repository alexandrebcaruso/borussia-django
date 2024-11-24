from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

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
