@echo off
echo ============================================
echo Django Inventory Management Setup
echo ============================================
echo.

REM Try to find Python executable (prefer Anaconda)
set PYTHON_CMD=
if exist "C:\Users\gtg09\anaconda3\python.exe" (
    set PYTHON_CMD=C:\Users\gtg09\anaconda3\python.exe
    echo Using: Anaconda Python 3.12
) else (
    where py >nul 2>&1
    if %errorlevel% == 0 (
        set PYTHON_CMD=py -3.12
        echo Using: py -3.12
    ) else (
        where python >nul 2>&1
        if %errorlevel% == 0 (
            set PYTHON_CMD=python
            echo Using: python
        ) else (
            echo ERROR: Python not found! Please install Python 3.8 or higher.
            pause
            exit /b 1
        )
    )
)

echo.
echo Step 1: Installing Django and dependencies...
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install django django-crispy-forms crispy-bootstrap5 Pillow
if errorlevel 1 (
    echo.
    echo ERROR: Failed to install packages.
    echo Trying with --user flag...
    %PYTHON_CMD% -m pip install --user django django-crispy-forms crispy-bootstrap5 Pillow
    if errorlevel 1 (
        echo Still failed. Please check Python installation.
        pause
        exit /b 1
    )
)

echo.
echo Step 2: Creating database migrations...
%PYTHON_CMD% manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

echo.
echo Step 3: Applying migrations to create database...
%PYTHON_CMD% manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next steps:
echo 1. Create an admin user (optional but recommended):
echo    %PYTHON_CMD% manage.py createsuperuser
echo.
echo 2. Start the server (use run_server.bat or):
echo    %PYTHON_CMD% manage.py runserver
echo.
echo Then open http://127.0.0.1:8000 in your browser
echo.
pause

