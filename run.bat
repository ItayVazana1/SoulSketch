@echo off
cd /d "%~dp0"
set PYTHONPATH=%cd%

echo ===============================
echo     SoulSketch Launcher
echo ===============================
echo.

REM === Step 0: Ensure shared_memory structure
call init_shared_memory_structure.bat

REM === Try to use py -3.10 explicitly if available
where py >nul 2>&1
IF %ERRORLEVEL%==0 (
    for /f %%i in ('py -3.10 --version 2^>nul') do (
        echo [INFO] Python 3.10 detected via py launcher.
        set PYTHON_CMD=py -3.10
    )
)

REM === Fallback: check "python" default version
IF NOT DEFINED PYTHON_CMD (
    for /f "tokens=2 delims= " %%i in ('python --version') do set PY_VER=%%i
    echo [INFO] Detected default python: %PY_VER%
    echo %PY_VER% | findstr /r "^3\.10" >nul
    IF %ERRORLEVEL%==0 (
        set PYTHON_CMD=python
    ) ELSE (
        echo [ERROR] Python 3.10 is not available or not default.
        echo [ACTION] Opening download page...
        start https://www.python.org/downloads/release/python-3100/
        pause
        exit /b
    )
)

REM === Create venv if not exists
IF NOT EXIST .venv (
    echo [INFO] Creating virtual environment...
    %PYTHON_CMD% -m venv .venv
)

REM === Activate venv
call .venv\Scripts\activate

REM === Check if streamlit is available
where .venv\Scripts\streamlit.exe >nul 2>&1
IF ERRORLEVEL 1 (
    echo [INFO] Installing requirements...
    pip install -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
)

REM === Launch app
echo.
echo [🚀] Running SoulSketch...
streamlit run app.py

pause
