@echo off
REM ===================================================================
REM Lumina Memory System - Quick Development Launcher
REM ===================================================================
REM Fast launcher for development work - minimal output
REM ===================================================================

cd /d "e:\lumina-memory-system"

REM Quick environment check
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found
    pause
    exit /b 1
)

REM Activate and launch
call venv\Scripts\activate.bat >nul 2>&1
if "%VIRTUAL_ENV%"=="" (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)

REM Set Python path for development
set PYTHONPATH=%CD%\src;%PYTHONPATH%

REM Launch GUI silently
python llm_consciousness_gui\main.py

REM Only show errors
if %ERRORLEVEL% neq 0 (
    echo ❌ Error code: %ERRORLEVEL%
    pause
)