@echo off
echo ========================================
echo   IR Search Engine - Installation Check
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is NOT installed!
    echo.
    echo Please install Python first:
    echo.
    echo Option 1: Download from https://www.python.org/downloads/
    echo           - Download Python 3.11 or 3.10
    echo           - IMPORTANT: Check "Add Python to PATH" during installation
    echo.
    echo Option 2: Install from Microsoft Store
    echo           - Open Microsoft Store
    echo           - Search "Python 3.11"
    echo           - Click Install
    echo.
    echo After installing Python, close this window and run this script again.
    echo.
    pause
    exit /b 1
)

echo [OK] Python is installed!
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is NOT installed!
    echo Installing pip...
    python -m ensurepip --upgrade
    echo.
)

echo [OK] pip is installed!
pip --version
echo.

echo ========================================
echo   Starting Installation...
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated!
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed!
echo.

echo Step 5: Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo [OK] NLTK data downloaded!
echo.

echo Step 6: Setting up database...
python manage.py migrate
if %errorlevel% neq 0 (
    echo [ERROR] Failed to setup database
    pause
    exit /b 1
)
echo [OK] Database setup complete!
echo.

echo Step 7: Creating superuser account...
echo.
echo Please create an admin account:
python manage.py createsuperuser
echo.

echo Step 8: Creating sample documents...
python manage.py create_sample_docs
echo [OK] Sample documents created!
echo.

echo Step 9: Building search index...
python manage.py index_docs
echo [OK] Search index built!
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo To start the server, run:
echo   start_server.bat
echo.
echo Or manually:
echo   venv\Scripts\activate
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/
echo.
pause
