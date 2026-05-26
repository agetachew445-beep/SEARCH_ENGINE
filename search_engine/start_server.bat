@echo off
echo ========================================
echo   Starting IR Search Engine Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Please run: check_and_install.bat first
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if Django is installed
python -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Django is not installed!
    echo Please run: check_and_install.bat first
    echo.
    pause
    exit /b 1
)

echo Starting Django development server...
echo.
echo Server will be available at:
echo   http://127.0.0.1:8000/
echo.
echo Admin panel:
echo   http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

python manage.py runserver

pause
