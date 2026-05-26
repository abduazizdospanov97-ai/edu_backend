import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create superuser from environment variables if not exists'

    def handle(self, *args, **kwargs):
        email = os.environ.get('ADMIN_EMAIL')
        password = os.environ.get('ADMIN_PASSWORD')
        name = os.environ.get('ADMIN_NAME', 'Admin')

        if not email or not password:
            self.stdout.write('ADMIN_EMAIL yoki ADMIN_PASSWORD topilmadi, o\'tkazib yuborildi.')
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(f'Superuser allaqachon mavjud: {email}')
            return

        User.objects.create_superuser(email=email, password=password, name=name)
        self.stdout.write(f'Superuser yaratildi: {email}')
