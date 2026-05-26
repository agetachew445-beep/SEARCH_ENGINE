@echo off
color 0A
echo.
echo  ╔══════════════════════════════════════════════════════════╗
echo  ║                                                          ║
echo  ║        IR SEARCH ENGINE - AUTOMATIC INSTALLER            ║
echo  ║                                                          ║
echo  ╚══════════════════════════════════════════════════════════╝
echo.
echo  This will:
echo  1. Check if Python is installed
echo  2. Install Python from Microsoft Store (if needed)
echo  3. Install all dependencies
echo  4. Setup database
echo  5. Create sample documents
echo  6. Build search index
echo  7. Start the server
echo.
echo  Press any key to start...
pause >nul

call AUTO_INSTALL_EVERYTHING.bat
