#!/bin/bash
# Setup script for IR Search Engine

echo "=== IR Search Engine Setup ==="
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser prompt
echo ""
echo "Create a superuser account for admin access:"
python manage.py createsuperuser

# Create sample documents
echo ""
echo "Creating sample documents..."
python manage.py create_sample_docs

# Build index
echo ""
echo "Building search index..."
python manage.py index_docs

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To start the development server:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/"
echo "Admin panel: http://127.0.0.1:8000/admin/"
