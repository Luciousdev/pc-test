@echo off

rem Set the log file path
set LOG_FILE=install.log

rem Function to log the output to the log file
:Log
echo %* >> %LOG_FILE%
echo %*
exit /b

rem Check if Python 3.11 is installed
py -3.11 -c "exit()" >nul 2>&1
if %errorlevel% equ 0 (
    call :Log Python 3.11 is already installed.
) else (
    call :Log Python 3.11 is not installed. Installing...
    
    REM Download Python 3.11 
    call :Log Downloading Python 3.11 installer...
    powershell -Command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe', 'python-3.11.0-amd64.exe')"
    
    rem Check if the download was successful
    IF NOT EXIST python-3.11.0-amd64.exe (
        call :Log Failed to download Python 3.11 installer.
        exit /b 1
    )
    
    call :Log Installing Python 3.11... This may take a while
    start /wait python-3.11.0-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
    
    rem Check if the installation was successful
    IF %errorlevel% neq 0 (
        call :Log Failed to install Python 3.11.
        exit /b 1
    )
    
    REM Delete the installer
    call :Log Deleting installer...
    del python-3.11.0-amd64.exe >nul 2>&1
    
    rem Check if the deletion was successful
    IF %errorlevel% neq 0 (
        call :Log Failed to delete the installer.
        exit /b 1
    )
    
    call :Log Python 3.11 has been installed.
)

rem Install requirements
call :Log Installing requirements...
pip install -r requirements.txt

rem Check if the installation was successful
IF %errorlevel% neq 0 (
    call :Log Failed to install requirements.
    exit /b 1
)

call :Log Requirements have been installed.

rem Execute get-data.py
call :Log Executing get-data.py...
python get-data.py

rem Check if the script execution was successful
IF %errorlevel% neq 0 (
    call :Log Failed to execute the script.
    exit /b 1
)

call :Log Script execution completed.

rem Exit the script
exit /b 0
