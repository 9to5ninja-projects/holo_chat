@echo off
REM ===================================================================
REM Lumina Memory System - GUI Launcher
REM ===================================================================
REM This batch file automatically activates the virtual environment
REM and launches the Enhanced LLM Consciousness GUI
REM ===================================================================

echo.
echo ========================================
echo  🚀 LUMINA MEMORY SYSTEM - GUI LAUNCHER
echo ========================================
echo.

REM Change to the project directory
cd /d "e:\lumina-memory-system"
echo 📁 Project directory: %CD%

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found at: venv\Scripts\activate.bat
    echo.
    echo 🔧 Please create a virtual environment first:
    echo    python -m venv venv
    echo    venv\Scripts\activate
    echo    pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if activation was successful
if "%VIRTUAL_ENV%"=="" (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

echo ✅ Virtual environment activated: %VIRTUAL_ENV%

REM Check if the GUI script exists
if not exist "llm_consciousness_gui\main.py" (
    echo ❌ GUI script not found at: llm_consciousness_gui\main.py
    echo.
    echo 🔍 Available files:
    dir llm_consciousness_gui\*.py
    echo.
    pause
    exit /b 1
)

echo 🎯 Launching Enhanced LLM Consciousness GUI...
echo.

REM Launch the GUI
python llm_consciousness_gui\main.py

REM Check exit code
if %ERRORLEVEL% neq 0 (
    echo.
    echo ❌ GUI exited with error code: %ERRORLEVEL%
    echo.
    echo 🔧 Common solutions:
    echo    - Check if all dependencies are installed: pip install -r requirements.txt
    echo    - Verify Python version compatibility
    echo    - Check for missing PySide6: pip install PySide6
    echo.
) else (
    echo.
    echo ✅ GUI closed successfully
)

echo.
echo 📝 Press any key to close this window...
pause >nul