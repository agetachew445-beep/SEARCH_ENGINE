#!/bin/bash
# Build script for Railway / Render deployment

echo "=== Installing dependencies ==="
pip install -r requirements.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Running migrations ==="
python manage.py migrate --noinput

echo "=== Creating superuser if not exists ==="
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Superuser created')
else:
    print('Superuser already exists')
"

echo "=== Loading sample documents ==="
python manage.py create_sample_docs
python manage.py add_local_docs

echo "=== Building search index ==="
python manage.py index_docs

echo "=== Build complete! ==="
