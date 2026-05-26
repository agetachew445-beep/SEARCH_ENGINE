@echo off
echo ========================================
echo   AUTO INSTALLER - IR Search Engine
echo ========================================
echo.

REM Try to run python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed yet.
    echo.
    echo Opening Microsoft Store to install Python...
    echo.
    echo INSTRUCTIONS:
    echo 1. Microsoft Store will open
    echo 2. Click "Get" or "Install" button
    echo 3. Wait for installation to complete
    echo 4. Close Microsoft Store
    echo 5. Run this script again
    echo.
    start ms-windows-store://pdp/?ProductId=9NRWMJP3717K
    pause
    exit /b 1
)

echo [OK] Python is installed!
python --version
echo.

echo ========================================
echo   Installing IR Search Engine...
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment
    echo Trying alternative method...
    python -m pip install virtualenv
    python -m virtualenv venv
)
echo [OK] Virtual environment created!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] pip upgraded!
echo.

echo Step 4: Installing Django and dependencies...
echo This may take 5-10 minutes...
pip install Django==4.2.7 --quiet
pip install nltk==3.8.1 --quiet
pip install scikit-learn==1.3.2 --quiet
pip install numpy==1.24.3 --quiet
pip install PyPDF2==3.0.1 --quiet
pip install beautifulsoup4==4.12.2 --quiet
echo [OK] All packages installed!
echo.

echo Step 5: Downloading NLTK data...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True)"
echo [OK] NLTK data downloaded!
echo.

echo Step 6: Setting up database...
python manage.py migrate --no-input
echo [OK] Database created!
echo.

echo Step 7: Creating sample documents...
python manage.py create_sample_docs
echo [OK] Sample documents created!
echo.

echo Step 8: Building search index...
python manage.py index_docs
echo [OK] Search index built!
echo.

echo ========================================
echo   Installation Complete!
echo ========================================
echo.
echo Now you need to create an admin account.
echo Please enter a username and password:
echo.
python manage.py createsuperuser
echo.

echo ========================================
echo   ALL DONE!
echo ========================================
echo.
echo To start the server, run:
echo   start_server.bat
echo.
echo Or press any key to start now...
pause

echo.
echo Starting server...
echo.
python manage.py runserver

pause
