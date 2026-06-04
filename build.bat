@echo off
REM ============================================
REM  F-Keyfy — Windows Build Script
REM  Run this from the project root folder.
REM ============================================

echo.
echo  === F-Keyfy Build ===
echo.

REM 1. Create a virtual environment (isolates dependencies = no conflicts)
if not exist "venv" (
    echo [1/4] Creating virtual environment...
    python -m venv venv
) else (
    echo [1/4] Virtual environment already exists.
)

REM 2. Activate and install dependencies
echo [2/4] Installing dependencies...
call venv\Scripts\activate.bat
pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
pip install pyinstaller >nul 2>&1

REM 3. Build with PyInstaller
echo [3/4] Building executable...
pyinstaller F-Keyfy.spec --noconfirm

REM 4. Done
echo.
echo [4/4] Build complete!
echo.
echo  Output:  dist\F-Keyfy\F-Keyfy.exe
echo  To distribute: zip the entire dist\F-Keyfy folder.
echo.
pause
