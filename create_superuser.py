import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
if not User.objects.filter(username='President').exists():
    User.objects.create_superuser('President', 'admin@example.com', 'Corporate17')
    print('Superuser created')
else:
    print('Superuser already exists')