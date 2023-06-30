@echo off

rem Check if Python 3.11 is installed
python --version 2>NUL | findstr /B "Python 3.11" >nul
if %errorlevel% equ 0 (
    echo Python 3.11 is already installed.
) else (
    echo Python 3.11 is not installed. Installing...
    
    REM Download Python 3.11 
    echo Downloading Python 3.11 installer...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe', 'python-3.11.0-amd64.exe')"
    
    echo Installing Python 3.11... This may take a while
    python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    
    REM Delete the installer
    echo Deleting installer...
    del python-3.11.0-amd64.exe

    echo Python 3.11 has been installed.
)

rem Install requirements
pip install -r requirements.txt

echo Requirements have been installed.

rem Execute get-data.py
python get-data.py

echo Script execution completed.
