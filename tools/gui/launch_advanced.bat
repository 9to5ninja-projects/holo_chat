@echo off
REM ===================================================================
REM Lumina Memory System - Advanced Launcher with Options
REM ===================================================================
REM This batch file provides multiple launch options and diagnostics
REM ===================================================================

:MAIN_MENU
cls
echo.
echo ========================================
echo  🚀 LUMINA MEMORY SYSTEM - ADVANCED LAUNCHER
echo ========================================
echo.
echo Please select an option:
echo.
echo 1. 🎯 Launch GUI (Standard)
echo 2. 🔧 Launch GUI with Debug Mode
echo 3. 📊 Run System Diagnostics
echo 4. 🧪 Launch Jupyter Notebooks
echo 5. 🔍 Check Dependencies
echo 6. 📝 View System Info
echo 7. ❌ Exit
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto LAUNCH_GUI
if "%choice%"=="2" goto LAUNCH_DEBUG
if "%choice%"=="3" goto DIAGNOSTICS
if "%choice%"=="4" goto LAUNCH_JUPYTER
if "%choice%"=="5" goto CHECK_DEPS
if "%choice%"=="6" goto SYSTEM_INFO
if "%choice%"=="7" goto EXIT
goto MAIN_MENU

:LAUNCH_GUI
echo.
echo 🎯 Launching GUI in Standard Mode...
cd /d "e:\lumina-memory-system"
call venv\Scripts\activate.bat
python llm_consciousness_gui\main.py
goto END

:LAUNCH_DEBUG
echo.
echo 🔧 Launching GUI in Debug Mode...
cd /d "e:\lumina-memory-system"
call venv\Scripts\activate.bat
set PYTHONPATH=%CD%\src;%PYTHONPATH%
python -u llm_consciousness_gui\main.py --debug
goto END

:DIAGNOSTICS
echo.
echo 📊 Running System Diagnostics...
cd /d "e:\lumina-memory-system"
call venv\Scripts\activate.bat
echo.
echo 🔍 Python Version:
python --version
echo.
echo 🔍 Virtual Environment:
echo %VIRTUAL_ENV%
echo.
echo 🔍 Installed Packages:
pip list | findstr -i "pyside6 numpy scipy"
echo.
echo 🔍 Project Structure:
if exist "src\lumina_memory" echo ✅ Core package found
if exist "llm_consciousness_gui" echo ✅ GUI package found
if exist "notebooks" echo ✅ Notebooks found
if exist "tests" echo ✅ Tests found
echo.
pause
goto MAIN_MENU

:LAUNCH_JUPYTER
echo.
echo 🧪 Launching Jupyter Notebooks...
cd /d "e:\lumina-memory-system"
call venv\Scripts\activate.bat
echo.
echo 🔄 Starting Jupyter Lab...
jupyter lab notebooks\
goto END

:CHECK_DEPS
echo.
echo 🔍 Checking Dependencies...
cd /d "e:\lumina-memory-system"
call venv\Scripts\activate.bat
echo.
echo 📦 Required packages:
pip check
echo.
echo 📋 All installed packages:
pip list
echo.
pause
goto MAIN_MENU

:SYSTEM_INFO
echo.
echo 📝 System Information:
echo =====================
echo.
echo 🖥️ Computer: %COMPUTERNAME%
echo 👤 User: %USERNAME%
echo 📅 Date: %DATE%
echo ⏰ Time: %TIME%
echo 🗂️ Current Directory: %CD%
echo 🐍 Python Path: %PYTHONPATH%
echo 🌐 Virtual Environment: %VIRTUAL_ENV%
echo.
echo 📁 Project Files:
dir /b *.py *.bat *.md 2>nul
echo.
pause
goto MAIN_MENU

:END
echo.
echo 📝 Press any key to return to menu or close window...
set /p return="Press Enter to return to menu (or close window): "
goto MAIN_MENU

:EXIT
echo.
echo 👋 Goodbye!
exit /b 0