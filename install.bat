@echo off
setlocal enabledelayedexpansion

:: ============================================================================
:: TDD-Style Pre-flight Checks and Bootstrapping
:: ============================================================================

:: 1. Administrator rights check.
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo [SETUP] This script requires administrator privileges.
    echo [SETUP] Attempting to restart as Administrator...
    echo.
    powershell -Command "Start-Process cmd.exe -Verb RunAs -ArgumentList '/k', '%~f0'"
    exit /b
)

:: At this point, we are running with administrator rights.
:: 2. Set console code page to UTF-8.
chcp 65001 > nul

:: 3. Network connectivity check.
echo [CHECK] Testing internet connectivity...
ping -n 1 8.8.8.8 >nul
if %errorlevel% neq 0 (
    echo [ERROR] No internet connection detected. Please check your network and try again.
    pause
    exit /b 1
)
echo [CHECK] Internet connection is OK.

:: 4. Robust Chocolatey Check and Install
echo [CHECK] Checking for Chocolatey package manager...
where choco >nul 2>nul
if %errorlevel% equ 0 goto :choco_functional_check

:install_choco
    echo [INSTALL] Chocolatey not found or broken. Attempting installation...
    powershell -NoProfile -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    
    echo [VERIFY] Verifying Chocolatey installation...
    if exist "%ProgramData%\chocolatey\helpers\refreshenv.cmd" (
        call "%ProgramData%\chocolatey\helpers\refreshenv.cmd" >nul 2>nul
    )
    where choco >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Chocolatey installation failed. The 'choco' command is still not available.
        echo [ADVICE] This is likely due to a previous broken installation at 'C:\ProgramData\chocolatey'.
        echo [ADVICE] Please follow these steps:
        echo [ADVICE] 1. Manually delete the folder 'C:\ProgramData\chocolatey'.
        echo [ADVICE] 2. Rerun this installation script.
        pause
        exit /b 1
    )

:choco_functional_check
    echo [VERIFY] Verifying Chocolatey functionality...
    choco -? >nul 2>nul
    if %errorlevel% neq 0 (
        echo [ERROR] Chocolatey appears to be installed but is not functional.
        echo [ADVICE] This points to a broken installation. Please follow these steps:
        echo [ADVICE] 1. Manually delete the folder 'C:\ProgramData\chocolatey'.
        echo [ADVICE] 2. Rerun this installation script.
        pause
        exit /b 1
    )
    echo [CHECK] Chocolatey is installed and functional.

:: 5. Check for and install Python using GOTO for robustness.
:python_check
echo [CHECK] Checking for Python...
where python >nul 2>nul
if %errorlevel% equ 0 goto :python_exists

    echo [INSTALL] Python not found. Installing with Chocolatey (this may take a few minutes)...
    choco install python -y
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install Python using Chocolatey.
        pause
        exit /b 1
    )
    goto :handover

:python_exists
echo [CHECK] Python is already installed.


:: ============================================================================
:: Handover to Main Python Script
:: ============================================================================
:handover
echo.
echo [INFO] Bootstrap successful. Handing over to the main Python installer script...
python "%~dp0install.py"
if %errorlevel% neq 0 (
    echo [ERROR] The main Python script reported an error.
    pause
    exit /b 1
)

:: Final pause for user to see the success message from Python script.
echo.
echo Script execution finished. Press any key to exit.
pause
endlocal