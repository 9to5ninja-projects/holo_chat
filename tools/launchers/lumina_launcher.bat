@echo off
setlocal enabledelayedexpansion
REM ===================================================================
REM Lumina Memory System - Unified Launcher
REM Professional launcher with integrated menu system
REM ===================================================================

:INIT
set "PROJECT_DIR=e:\lumina-memory-system"
set "VENV_PATH=%PROJECT_DIR%\venv"
set "GUI_SCRIPT=%PROJECT_DIR%\llm_consciousness_gui\main.py"
set "VERSION=1.0.0"

REM Change to project directory
cd /d "%PROJECT_DIR%"

:MAIN_MENU
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🧠 LUMINA MEMORY SYSTEM - UNIFIED LAUNCHER v%VERSION%        ║
echo ║                                                              ║
echo ║    Enhanced LLM Consciousness GUI with XPUnit Analysis      ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo ┌──────────────────────────────────────────────────────────────┐
echo │                        LAUNCH OPTIONS                        │
echo └──────────────────────────────────────────────────────────────┘
echo.
echo   1. 🚀 Launch GUI (Standard Mode)
echo      └─ Start the Enhanced LLM Consciousness GUI with Holographic Memory
echo.
echo   2. 🔧 Launch GUI (Debug Mode)  
echo      └─ Start with verbose logging and debug information
echo.
echo   3. 🧪 Launch Jupyter Notebooks
echo      └─ Open Jupyter Lab for notebook development
echo.
echo   4. 📊 System Diagnostics
echo      └─ Check environment, dependencies, and system health
echo.
echo   5. 🧠 Test Holographic Memory
echo      └─ Run holographic memory integration tests
echo.
echo   6. 🤖 Interactive LLM Memory Testing
echo      └─ Test memory formation with real conversations
echo.
echo   7. ⚙️  Environment Setup
echo      └─ Install/update virtual environment and dependencies
echo.
echo   8. 🔗 Create Desktop Shortcut
echo      └─ Add launcher shortcut to desktop
echo.
echo   9. ❌ Exit
echo      └─ Close launcher
echo.
echo ┌──────────────────────────────────────────────────────────────┐
set /p "choice=│ Enter your choice (1-9): "
echo └──────────────────────────────────────────────────────────────┘

if "%choice%"=="1" goto LAUNCH_STANDARD
if "%choice%"=="2" goto LAUNCH_DEBUG
if "%choice%"=="3" goto LAUNCH_JUPYTER
if "%choice%"=="4" goto DIAGNOSTICS
if "%choice%"=="5" goto TEST_HOLOGRAPHIC
if "%choice%"=="6" goto TEST_LLM_MEMORY
if "%choice%"=="7" goto SETUP_ENV
if "%choice%"=="8" goto CREATE_SHORTCUT
if "%choice%"=="9" goto EXIT

echo.
echo ❌ Invalid choice. Please enter 1-9.
timeout /t 2 >nul
goto MAIN_MENU

:LAUNCH_STANDARD
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    🚀 LAUNCHING GUI (STANDARD)               ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
call :CHECK_ENVIRONMENT
if !ERRORLEVEL! neq 0 goto MAIN_MENU

echo 🎯 Starting Enhanced LLM Consciousness GUI...
echo.
call "%VENV_PATH%\Scripts\activate.bat"
python "%GUI_SCRIPT%"

call :HANDLE_EXIT_CODE
goto MAIN_MENU

:LAUNCH_DEBUG
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     🔧 LAUNCHING GUI (DEBUG)                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
call :CHECK_ENVIRONMENT
if !ERRORLEVEL! neq 0 goto MAIN_MENU

echo 🔍 Starting GUI with debug mode enabled...
echo 📝 Debug information will be displayed in console
echo.
call "%VENV_PATH%\Scripts\activate.bat"
set PYTHONPATH=%PROJECT_DIR%\src;%PYTHONPATH%
python -u "%GUI_SCRIPT%" --debug

call :HANDLE_EXIT_CODE
goto MAIN_MENU

:LAUNCH_JUPYTER
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   🧪 LAUNCHING JUPYTER LAB                  ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
call :CHECK_ENVIRONMENT
if !ERRORLEVEL! neq 0 goto MAIN_MENU

echo 📚 Starting Jupyter Lab for notebook development...
echo 🌐 Browser will open automatically
echo.
call "%VENV_PATH%\Scripts\activate.bat"
jupyter lab notebooks\

call :HANDLE_EXIT_CODE
goto MAIN_MENU

:DIAGNOSTICS
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                     📊 SYSTEM DIAGNOSTICS                   ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 ENVIRONMENT CHECK:
echo ────────────────────────────────────────────────────────────────
echo 📁 Project Directory: %PROJECT_DIR%
if exist "%PROJECT_DIR%" (echo ✅ Project directory found) else (echo ❌ Project directory not found)

echo.
echo 🐍 PYTHON INSTALLATION:
echo ────────────────────────────────────────────────────────────────
python --version 2>nul && echo ✅ Python found || echo ❌ Python not found in PATH

echo.
echo 🌐 VIRTUAL ENVIRONMENT:
echo ────────────────────────────────────────────────────────────────
if exist "%VENV_PATH%\Scripts\activate.bat" (
    echo ✅ Virtual environment found
    call "%VENV_PATH%\Scripts\activate.bat"
    echo 📍 Environment: %VIRTUAL_ENV%
) else (
    echo ❌ Virtual environment not found
)

echo.
echo 📦 KEY PACKAGES:
echo ────────────────────────────────────────────────────────────────
python -c "import PySide6; print('✅ PySide6:', PySide6.__version__)" 2>nul || echo "❌ PySide6 not installed"
python -c "import numpy; print('✅ NumPy:', numpy.__version__)" 2>nul || echo "❌ NumPy not installed"
python -c "import scipy; print('✅ SciPy:', scipy.__version__)" 2>nul || echo "❌ SciPy not installed"

echo.
echo 🧪 GUI IMPORT TEST:
echo ────────────────────────────────────────────────────────────────
python -c "from llm_consciousness_gui.main import main; print('✅ GUI import successful')" 2>nul || echo "❌ GUI import failed"

echo.
echo 📋 PROJECT STRUCTURE:
echo ────────────────────────────────────────────────────────────────
if exist "src\lumina_memory" echo ✅ Core package found
if exist "llm_consciousness_gui" echo ✅ GUI package found  
if exist "notebooks" echo ✅ Notebooks found
if exist "tests" echo ✅ Tests found

echo.
echo ────────────────────────────────────────────────────────────────
pause
goto MAIN_MENU

:TEST_HOLOGRAPHIC
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   🧠 TESTING HOLOGRAPHIC MEMORY              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
call :CHECK_ENVIRONMENT
if !ERRORLEVEL! neq 0 goto MAIN_MENU

echo 🧪 Running holographic memory integration tests...
echo 📊 This will test HRR operations, consciousness analysis, and capacity
echo.
call "%VENV_PATH%\Scripts\activate.bat"
python test_holographic_integration.py

call :HANDLE_EXIT_CODE
goto MAIN_MENU

:TEST_LLM_MEMORY
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                🤖 INTERACTIVE LLM MEMORY TESTING             ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
call :CHECK_ENVIRONMENT
if !ERRORLEVEL! neq 0 goto MAIN_MENU

echo 🤖 Starting interactive LLM memory testing session...
echo 💬 This will test memory formation using real conversations
echo 📊 Features: emotional analysis, contextual relationships, recall testing
echo.
echo 🎯 You can have conversations and test how memories are formed!
echo.
call "%VENV_PATH%\Scripts\activate.bat"
python interactive_llm_memory_test.py

call :HANDLE_EXIT_CODE
goto MAIN_MENU

:SETUP_ENV
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                    ⚙️  ENVIRONMENT SETUP                     ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

echo 🔍 Checking Python installation...
python --version >nul 2>&1
if !ERRORLEVEL! neq 0 (
    echo ❌ Python not found in PATH
    echo 🔧 Please install Python 3.8+ and add it to PATH
    pause
    goto MAIN_MENU
)
python --version
echo ✅ Python found

echo.
echo 🔄 Setting up virtual environment...
if not exist "%VENV_PATH%" (
    echo 📦 Creating virtual environment...
    python -m venv "%VENV_PATH%"
    if !ERRORLEVEL! neq 0 (
        echo ❌ Failed to create virtual environment
        pause
        goto MAIN_MENU
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo 🔄 Activating virtual environment...
call "%VENV_PATH%\Scripts\activate.bat"
echo ✅ Environment activated

echo.
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

echo.
echo 📦 Installing dependencies...
if exist "requirements.txt" (
    echo 🔄 Installing from requirements.txt...
    pip install -r requirements.txt
)

if exist "requirements-dev.txt" (
    echo 🔄 Installing development requirements...
    pip install -r requirements-dev.txt
)

if exist "setup.py" (
    echo 🔄 Installing package in development mode...
    pip install -e .
)

echo.
echo ✅ Environment setup complete!
echo.
pause
goto MAIN_MENU

:CREATE_SHORTCUT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                   🔗 CREATE DESKTOP SHORTCUT                ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT_NAME=Lumina Memory System.lnk"

echo 🔗 Creating desktop shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\%SHORTCUT_NAME%'); $Shortcut.TargetPath = '%~f0'; $Shortcut.WorkingDirectory = '%PROJECT_DIR%'; $Shortcut.Description = 'Lumina Memory System - Enhanced LLM Consciousness GUI'; $Shortcut.Save()}"

if exist "%DESKTOP%\%SHORTCUT_NAME%" (
    echo ✅ Desktop shortcut created successfully!
    echo 📍 Location: %DESKTOP%\%SHORTCUT_NAME%
    echo.
    echo 🎯 You can now double-click the desktop shortcut to launch this menu
) else (
    echo ❌ Failed to create desktop shortcut
)

echo.
pause
goto MAIN_MENU

:CHECK_ENVIRONMENT
echo 🔍 Checking environment...
if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo ❌ Virtual environment not found
    echo 🔧 Please run option 5 (Environment Setup) first
    echo.
    pause
    exit /b 1
)

if not exist "%GUI_SCRIPT%" (
    echo ❌ GUI script not found at: %GUI_SCRIPT%
    echo.
    pause
    exit /b 1
)

echo ✅ Environment check passed
exit /b 0

:HANDLE_EXIT_CODE
echo.
if %ERRORLEVEL% neq 0 (
    echo ❌ Application exited with error code: %ERRORLEVEL%
    echo.
    echo 🔧 Common solutions:
    echo    • Run option 5 (Environment Setup) to install dependencies
    echo    • Run option 4 (System Diagnostics) to check for issues
    echo    • Check if all required packages are installed
) else (
    echo ✅ Application closed successfully
)
echo.
echo 📝 Press any key to return to menu...
pause >nul
exit /b 0

:EXIT
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                    👋 Thank you for using                    ║
echo ║                  LUMINA MEMORY SYSTEM                        ║
echo ║                                                              ║
echo ║              Enhanced LLM Consciousness GUI                  ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
timeout /t 2 >nul
exit /b 0