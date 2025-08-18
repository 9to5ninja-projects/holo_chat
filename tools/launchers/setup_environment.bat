@echo off
REM ===================================================================
REM Lumina Memory System - Environment Setup Script
REM ===================================================================
REM This script sets up the complete development environment
REM ===================================================================

echo.
echo ========================================
echo  🔧 LUMINA MEMORY SYSTEM - ENVIRONMENT SETUP
echo ========================================
echo.

cd /d "e:\lumina-memory-system"

echo 📁 Working directory: %CD%
echo.

REM Check Python installation
echo 🐍 Checking Python installation...
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ❌ Python not found in PATH
    echo 🔧 Please install Python 3.8+ and add it to PATH
    pause
    exit /b 1
)

python --version
echo ✅ Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 🔄 Creating virtual environment...
    python -m venv venv
    if %ERRORLEVEL% neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if "%VIRTUAL_ENV%"=="" (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip
echo.

REM Install requirements
if exist "requirements.txt" (
    echo 📦 Installing requirements from requirements.txt...
    pip install -r requirements.txt
    echo.
)

if exist "requirements-dev.txt" (
    echo 📦 Installing development requirements...
    pip install -r requirements-dev.txt
    echo.
)

REM Install package in development mode
if exist "setup.py" (
    echo 📦 Installing package in development mode...
    pip install -e .
    echo.
)

REM Verify key packages
echo 🔍 Verifying key packages...
python -c "import PySide6; print('✅ PySide6:', PySide6.__version__)" 2>nul || echo "❌ PySide6 not found"
python -c "import numpy; print('✅ NumPy:', numpy.__version__)" 2>nul || echo "❌ NumPy not found"
python -c "import scipy; print('✅ SciPy:', scipy.__version__)" 2>nul || echo "❌ SciPy not found"
echo.

REM Test GUI import
echo 🧪 Testing GUI import...
python -c "from llm_consciousness_gui.main import main; print('✅ GUI import successful')" 2>nul || echo "❌ GUI import failed"
echo.

echo ========================================
echo  ✅ SETUP COMPLETE!
echo ========================================
echo.
echo 🎯 You can now use:
echo    • launch_gui.bat - Standard GUI launcher
echo    • launch_advanced.bat - Advanced launcher with options
echo    • dev_launch.bat - Quick development launcher
echo.
echo 🔗 Run create_desktop_shortcut.bat to create a desktop shortcut
echo.
pause