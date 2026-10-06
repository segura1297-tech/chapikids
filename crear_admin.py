import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chapikids.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@chapikids.com')
password = os.environ.get('ADMIN_PASSWORD', '')

if password and not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'OK: superusuario "{username}" creado')
else:
    print(f'OK: superusuario "{username}" ya existe o sin password')
