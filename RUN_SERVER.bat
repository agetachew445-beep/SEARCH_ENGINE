@echo off
title IR Search Engine
color 0A
cls

echo.
echo  ==========================================
echo   IR Search Engine - Starting...
echo  ==========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo  [ERROR] Virtual environment not found!
    echo  Please run: check_and_install.bat first
    pause
    exit /b 1
)

echo  Server starting on http://127.0.0.1:8000/
echo.
echo  Pages:
echo    Search:    http://127.0.0.1:8000/
echo    Login:     http://127.0.0.1:8000/login/
echo    Documents: http://127.0.0.1:8000/documents/
echo    Add Doc:   http://127.0.0.1:8000/upload/
echo    Admin:     http://127.0.0.1:8000/admin/
echo.
echo  Admin credentials:  admin / admin123
echo  Press Ctrl+C to stop
echo  ==========================================
echo.

start "" "http://127.0.0.1:8000/"

venv\Scripts\python.exe manage.py runserver 8000

pause
