@echo off
title Push to GitHub
color 0B
cls

echo.
echo  ==========================================
echo   Push IR Search Engine to GitHub
echo  ==========================================
echo.

cd /d "%~dp0"

echo  Step 1: Enter your GitHub details
echo  ==========================================
echo.

set /p GITHUB_USER=Enter your GitHub username: 
set /p GITHUB_REPO=Enter repository name (press Enter for: ir-search-engine): 

if "%GITHUB_REPO%"=="" set GITHUB_REPO=ir-search-engine

echo.
echo  Your repository URL will be:
echo  https://github.com/%GITHUB_USER%/%GITHUB_REPO%.git
echo.
echo  Step 2: Connecting to GitHub...
echo  ==========================================

git remote remove origin 2>nul
git remote add origin https://github.com/%GITHUB_USER%/%GITHUB_REPO%.git

echo  [OK] Remote added!
echo.
echo  Step 3: Pushing code to GitHub...
echo  ==========================================
echo.
echo  NOTE: When asked for password, use your
echo  GitHub Personal Access Token (NOT your password)
echo  Get token at: https://github.com/settings/tokens
echo.

git push -u origin master

if %errorlevel% equ 0 (
    echo.
    echo  ==========================================
    echo   SUCCESS! Code pushed to GitHub!
    echo  ==========================================
    echo.
    echo  Your GitHub repo:
    echo  https://github.com/%GITHUB_USER%/%GITHUB_REPO%
    echo.
    echo  Next step: Go to https://render.com
    echo  and connect this repository.
    echo.
) else (
    echo.
    echo  ==========================================
    echo   PUSH FAILED - Common fixes:
    echo  ==========================================
    echo.
    echo  1. Make sure the repository exists on GitHub
    echo     Go to: https://github.com/new
    echo     Name it: %GITHUB_REPO%
    echo.
    echo  2. For password - use Personal Access Token
    echo     Go to: https://github.com/settings/tokens
    echo     Click "Generate new token (classic)"
    echo     Check "repo" permission
    echo     Copy the token and use it as password
    echo.
    echo  3. Run this file again after fixing
    echo.
)

pause
