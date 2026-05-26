@echo off
REM Setup script for IR Search Engine (Windows)

echo === IR Search Engine Setup ===
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Download NLTK data
echo Downloading NLTK data...
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

REM Run migrations
echo Running database migrations...
python manage.py migrate

REM Create superuser
echo.
echo Create a superuser account for admin access:
python manage.py createsuperuser

REM Create sample documents
echo.
echo Creating sample documents...
python manage.py create_sample_docs

REM Build index
echo.
echo Building search index...
python manage.py index_docs

echo.
echo === Setup Complete! ===
echo.
echo To start the development server:
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
pause
