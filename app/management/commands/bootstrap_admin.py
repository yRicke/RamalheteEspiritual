import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Create or update the production superuser from environment variables.'

    def handle(self, *args, **options):
        username = os.getenv('ADMIN_USERNAME', 'admin').strip()
        password = os.getenv('ADMIN_PASSWORD', '')

        if not username or not password:
            raise CommandError('ADMIN_USERNAME and ADMIN_PASSWORD must be configured.')

        user, created = User.objects.get_or_create(username=username)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()

        action = 'created' if created else 'updated'
        self.stdout.write(self.style.SUCCESS(f'Superuser {username} {action}.'))
