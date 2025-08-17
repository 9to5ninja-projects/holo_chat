#!/usr/bin/env python3
"""
Build Lumina Launcher Executable
================================
This script creates a standalone executable from the Python launcher
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print(f"✅ PyInstaller found: {PyInstaller.__version__}")
        return True
    except ImportError:
        print("❌ PyInstaller not found")
        print("🔧 Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def create_spec_file():
    """Create PyInstaller spec file for customization"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['lumina_launcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'threading',
        'webbrowser',
        'pathlib',
        'subprocess'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='LuminaLauncher',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Set to True for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)
'''
    
    with open('lumina_launcher.spec', 'w') as f:
        f.write(spec_content)
    print("✅ Spec file created: lumina_launcher.spec")

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building executable...")
    
    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window
        "--name", "LuminaLauncher",     # Executable name
        "--clean",                      # Clean build
        "lumina_launcher.py"
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_installer_package():
    """Create a complete installer package"""
    print("📦 Creating installer package...")
    
    # Create package directory
    package_dir = Path("LuminaMemorySystem_Installer")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    exe_path = Path("dist") / "LuminaLauncher.exe"
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir / "LuminaLauncher.exe")
        print(f"✅ Copied executable to {package_dir}")
    else:
        print("❌ Executable not found in dist/")
        return False
    
    # Create installer script
    installer_script = package_dir / "install.bat"
    installer_content = '''@echo off
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║    🧠 LUMINA MEMORY SYSTEM - INSTALLER                       ║
echo ║                                                              ║
echo ║    Enhanced LLM Consciousness GUI Installation               ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.

set "INSTALL_DIR=%USERPROFILE%\\LuminaMemorySystem"
set "DESKTOP=%USERPROFILE%\\Desktop"

echo 📁 Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo ✅ Created installation directory
) else (
    echo ✅ Installation directory exists
)

REM Copy launcher
copy "LuminaLauncher.exe" "%INSTALL_DIR%\\LuminaLauncher.exe" >nul
if %ERRORLEVEL% equ 0 (
    echo ✅ Launcher installed successfully
) else (
    echo ❌ Failed to install launcher
    pause
    exit /b 1
)

REM Create desktop shortcut
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\\Lumina Memory System.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\LuminaLauncher.exe'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'Lumina Memory System - Enhanced LLM Consciousness GUI'; $Shortcut.Save()}"

if exist "%DESKTOP%\\Lumina Memory System.lnk" (
    echo ✅ Desktop shortcut created
) else (
    echo ⚠️ Desktop shortcut creation failed
)

REM Add to Start Menu (optional)
set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
copy "%DESKTOP%\\Lumina Memory System.lnk" "%START_MENU%\\Lumina Memory System.lnk" >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo ✅ Start menu shortcut created
)

echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║                                                              ║
echo ║                    ✅ INSTALLATION COMPLETE!                 ║
echo ║                                                              ║
echo ║    You can now launch Lumina Memory System from:            ║
echo ║    • Desktop shortcut                                       ║
echo ║    • Start menu                                             ║
echo ║    • %INSTALL_DIR%\\LuminaLauncher.exe                        ║
echo ║                                                              ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
pause
'''
    
    with open(installer_script, 'w') as f:
        f.write(installer_content)
    
    # Create README
    readme_content = '''# Lumina Memory System - Installer Package

## Installation Instructions

1. **Run the installer:**
   - Double-click `install.bat`
   - Follow the on-screen instructions

2. **Launch the application:**
   - Use the desktop shortcut "Lumina Memory System"
   - Or find it in the Start menu
   - Or run directly from: `%USERPROFILE%\\LuminaMemorySystem\\LuminaLauncher.exe`

## What gets installed:

- **LuminaLauncher.exe** - The main launcher application
- **Desktop shortcut** - For easy access
- **Start menu entry** - For quick launching

## Features:

- 🚀 Launch GUI (Standard Mode)
- 🔧 Launch GUI (Debug Mode)  
- 🧪 Launch Jupyter Notebooks
- 📊 System Diagnostics
- ⚙️ Environment Setup
- 🔗 Desktop Shortcut Creation

## Requirements:

- Windows 10/11
- Python 3.8+ (for development features)
- Internet connection (for initial setup)

## Support:

For issues or questions, please refer to the project documentation.
'''
    
    with open(package_dir / "README.txt", 'w') as f:
        f.write(readme_content)
    
    print(f"✅ Installer package created: {package_dir}")
    print(f"📁 Contents:")
    for item in package_dir.iterdir():
        print(f"   - {item.name}")
    
    return True

def main():
    """Main build process"""
    print("🔨 LUMINA LAUNCHER - EXECUTABLE BUILD PROCESS")
    print("=" * 60)
    print()
    
    # Check PyInstaller
    if not check_pyinstaller():
        return 1
    
    print()
    
    # Build executable
    if not build_executable():
        return 1
    
    print()
    
    # Create installer package
    if not create_installer_package():
        return 1
    
    print()
    print("🎉 BUILD PROCESS COMPLETE!")
    print("=" * 60)
    print()
    print("📦 Your installer package is ready:")
    print("   📁 LuminaMemorySystem_Installer/")
    print("   ├── 🚀 LuminaLauncher.exe")
    print("   ├── 📜 install.bat")
    print("   └── 📖 README.txt")
    print()
    print("🎯 To distribute:")
    print("   1. Zip the 'LuminaMemorySystem_Installer' folder")
    print("   2. Share the zip file with users")
    print("   3. Users run 'install.bat' to install")
    print()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())