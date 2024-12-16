from django.core.management.base import BaseCommand
from agua.models import Role

class Command(BaseCommand):
    help = 'Create default roles'

    def handle(self, *args, **kwargs):
        roles = ['Admin', 'ApplicationAdmin', 'RegularUser']
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)
            self.stdout.write(self.style.SUCCESS(f'Created role: {role_name}'))
            