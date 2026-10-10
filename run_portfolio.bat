@echo off
setlocal
cd /d "%~dp0"

set "PY="
where py >nul 2>nul
if not errorlevel 1 (
    py -c "import sys" >nul 2>nul
    if not errorlevel 1 set "PY=py"
)

if not defined PY (
    where python >nul 2>nul
    if not errorlevel 1 (
        python -c "import sys" >nul 2>nul
        if not errorlevel 1 set "PY=python"
    )
)

if not defined PY (
    echo Python 3 was not found. Install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

%PY% -c "import flask" >nul 2>nul
if errorlevel 1 (
    echo Flask was not found. Installing Flask now...
    %PY% -m pip install Flask
    if errorlevel 1 (
        echo Could not install Flask. Install it manually with: python -m pip install Flask
        pause
        exit /b 1
    )
)

echo Starting the Flask portfolio...
echo If the browser does not open, visit: http://127.0.0.1:5000
start "" powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -Command "Start-Sleep -Seconds 2; Start-Process 'http://127.0.0.1:5000'"
%PY% "%~dp0portfolio_app.py"
pause
