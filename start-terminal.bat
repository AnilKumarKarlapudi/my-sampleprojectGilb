@echo off
SETLOCAL enabledelayedexpansion

REM Check python version
call :Logger "INFO" "Checking for required python version..."
python resources\bin\deployment\check-python-version.py
call :CheckIfExists "python.exe" "D:\Python" OK
if "!OK!"=="0" (
    call :Logger "ERROR" "Unable to check/install required python version!"
    exit /b %errorlevel%
)

REM Check if virtual env exists
call :Logger "INFO" "Checking if venv exists in root..."
call :CheckIfExists "venv" "%cd%" OK

REM Create virtual env if it does not exist
if "!OK!"=="0" (
    call :Logger "WARNING" "Virtual environment does not exist, creating a new one..."
    REM TODO: We should check if this is correct...
    D:\Python\python.exe -m venv venv/

    call :CheckIfExists "venv" "%cd%" OK
    if "!OK!"=="0" (
        call :Logger "ERROR" "Unable to create virtual env!"
        exit /b %errorlevel%
    )
)

REM Upgrade PIP and install requirements before activating the venv...
.\venv\Scripts\python.exe -m pip install --upgrade pip
.\venv\Scripts\python.exe -m pip install -r requirements.txt

REM Check for selenium just in case...
.\venv\Scripts\python.exe .\resources\bin\selenium-check.py

REM Setup IPs
.\venv\Scripts\python.exe .\resources\bin\utility\servers\main.py

REM Activate virtual env and start a new cmd shell...
call :Logger "INFO" "Activating virtual environment..."
start .\venv\Scripts\activate.bat
exit /b 0

:Logger
for /f "tokens=* usebackq" %%f in (`date /t`) do (set dt=%%f)
for /f "tokens=* usebackq" %%f in (`time /t`) do (set tm=%%f)
echo %dt%%tm% [%~1] (start-terminal) - %~2
exit /b

:CheckIfExists
set "IT_EXISTS=0"
for /f %%f in ('dir /b /a %~2') do (
    echo %%~f
    if "%%~f"=="%~1" (
        set "IT_EXISTS=1"
    )
)
set /a "%~3=!IT_EXISTS!"
exit /b 0

ENDLOCAL