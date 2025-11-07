@echo off
setlocal

:: 1. Administrator rights check. All non-ASCII characters are removed to prevent encoding issues.
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo.
    echo This script requires administrator privileges.
    echo Attempting to restart as Administrator...
    echo.
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

:: 2. Set console code page to UTF-8 for the Python script's output.
chcp 65001 > nul

:: 3. Execute the main Python installation script.
python "%~dp0install.py"

:: 4. Pause at the end to allow the user to see the final message from the Python script.
echo.
echo Script execution finished. Press any key to exit.
pause
endlocal