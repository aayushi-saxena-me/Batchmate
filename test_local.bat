@echo off
echo ============================================
echo Testing Django Inventory Management
echo ============================================
echo.

REM Use Python 3.12 launcher
set PYTHON_CMD=py -3.12

echo Step 1: Checking Django installation...
%PYTHON_CMD% -m django --version
if errorlevel 1 (
    echo ERROR: Django not installed!
    pause
    exit /b 1
)

echo.
echo Step 2: Checking database migrations...
%PYTHON_CMD% manage.py makemigrations --dry-run
if errorlevel 1 (
    echo WARNING: Migration check failed
)

echo.
echo Step 3: Applying migrations...
%PYTHON_CMD% manage.py migrate
if errorlevel 1 (
    echo ERROR: Migrations failed!
    pause
    exit /b 1
)

echo.
echo Step 4: Checking for superusers...
%PYTHON_CMD% manage.py shell -c "from django.contrib.auth.models import User; count = User.objects.filter(is_superuser=True).count(); print(f'Found {count} superuser(s)'); exit(0 if count > 0 else 1)"
if errorlevel 1 (
    echo.
    echo No superuser found. You may want to create one with:
    echo   %PYTHON_CMD% manage.py createsuperuser
    echo.
)

echo.
echo Step 5: Running Django system check...
%PYTHON_CMD% manage.py check
if errorlevel 1 (
    echo WARNING: System check found issues
) else (
    echo System check passed!
)

echo.
echo ============================================
echo Testing Complete!
echo ============================================
echo.
echo To start the server, run:
echo   %PYTHON_CMD% manage.py runserver
echo.
echo Or use: run_server.bat
echo.
pause

