@echo off
REM Run all tests for IR Search Engine

echo === Running IR Search Engine Tests ===
echo.

REM Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
)

echo Running Django tests...
python manage.py test

echo.
echo === Test Summary ===
echo Check output above for results
echo.

pause
