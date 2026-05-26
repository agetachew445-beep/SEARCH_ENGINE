@echo off
title IR Search Engine - One-Click Installer
color 0B

cls
echo.
echo  ╔════════════════════════════════════════════════════════════════╗
echo  ║                                                                ║
echo  ║           IR SEARCH ENGINE - ONE-CLICK INSTALLER               ║
echo  ║                                                                ║
echo  ║  This will automatically install everything you need!          ║
echo  ║                                                                ║
echo  ╚════════════════════════════════════════════════════════════════╝
echo.
echo  What this does:
echo  ───────────────
echo  ✓ Installs Python (if needed)
echo  ✓ Installs all dependencies
echo  ✓ Sets up database
echo  ✓ Creates sample documents
echo  ✓ Builds search index
echo  ✓ Starts the server
echo.
echo  Time required: 10-15 minutes
echo.
echo  ════════════════════════════════════════════════════════════════
echo.
echo  Press any key to begin installation...
echo.
pause >nul

call AUTO_INSTALL_EVERYTHING.bat
