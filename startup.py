"""
Startup script — runs on Railway after migrations.
Creates the admin superuser if it doesn't exist.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'search_engine.settings')
django.setup()

from django.contrib.auth.models import User

username = os.environ.get('ADMIN_USERNAME', 'admin')
password = os.environ.get('ADMIN_PASSWORD', 'admin123')
email    = os.environ.get('ADMIN_EMAIL', 'admin@irsearch.com')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'✅ Superuser "{username}" created.')
else:
    print(f'ℹ️  Superuser "{username}" already exists.')
