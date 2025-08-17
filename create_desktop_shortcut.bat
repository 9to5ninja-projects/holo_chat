@echo off
REM ===================================================================
REM Create Desktop Shortcut for Lumina Memory System GUI
REM ===================================================================

echo.
echo 🔗 Creating Desktop Shortcut...
echo.

REM Get desktop path
set DESKTOP=%USERPROFILE%\Desktop

REM Create shortcut using PowerShell
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\Lumina Memory GUI.lnk'); $Shortcut.TargetPath = '%CD%\launch_gui.bat'; $Shortcut.WorkingDirectory = '%CD%'; $Shortcut.Description = 'Launch Lumina Memory System GUI'; $Shortcut.Save()}"

if exist "%DESKTOP%\Lumina Memory GUI.lnk" (
    echo ✅ Desktop shortcut created successfully!
    echo 📍 Location: %DESKTOP%\Lumina Memory GUI.lnk
    echo.
    echo 🎯 You can now double-click the desktop shortcut to launch the GUI
) else (
    echo ❌ Failed to create desktop shortcut
    echo 🔧 You can manually create a shortcut to: %CD%\launch_gui.bat
)

echo.
pause