# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

## Step-by-Step Installation

### 1. Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd search_engine

# Or download and extract the ZIP file
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

Or run Python interactively:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

### 5. Setup Database

```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Create Sample Documents (Optional)

```bash
python manage.py create_sample_docs
```

This creates 8 sample documents about IR concepts.

### 8. Build Search Index

```bash
python manage.py index_docs
```

This builds the inverted index and computes TF-IDF weights.

### 9. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## Quick Setup (Automated)

**Windows:**
```bash
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

## Troubleshooting

### Issue: Django not found
```bash
pip install Django==4.2.7
```

### Issue: NLTK data not found
```python
import nltk
nltk.download('all')  # Download all NLTK data
```

### Issue: Port 8000 already in use
```bash
python manage.py runserver 8080
```

### Issue: Database locked
```bash
# Delete db.sqlite3 and recreate
rm db.sqlite3
python manage.py migrate
```

## Next Steps

1. **Add Documents**: Go to http://127.0.0.1:8000/admin/
2. **Build Index**: Run `python manage.py index_docs`
3. **Search**: Visit http://127.0.0.1:8000/
4. **Evaluate**: Run `python manage.py evaluate_search`

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL instead of SQLite
4. Collect static files: `python manage.py collectstatic`
5. Use Gunicorn: `gunicorn search_engine.wsgi:application`
6. Setup Nginx as reverse proxy

## Support

For issues or questions, refer to:
- Django documentation: https://docs.djangoproject.com/
- NLTK documentation: https://www.nltk.org/
- Project README.md
