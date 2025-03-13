from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    roles = models.ManyToManyField('Role', related_name='users')

    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_superuser:
            admin_role, created_admin = Role.objects.get_or_create(name='Admin')
            app_admin_role, created_app_admin = Role.objects.get_or_create(name='Application admin')
            self.roles.add(admin_role, app_admin_role)

class Role(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
