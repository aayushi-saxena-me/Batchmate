@echo off
echo ========================================
echo Starting Inventory Management Application
echo ========================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate venv and install dependencies
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Checking if Django is installed...
venv\Scripts\python.exe -c "import django" 2>nul
if errorlevel 1 (
    echo Django not found. Installing dependencies...
    pip install -r requirements.txt
) else (
    echo Django is already installed.
)

echo.
echo Running migrations...
python manage.py migrate

echo.
echo ========================================
echo Starting development server...
echo ========================================
echo.
echo Server will be available at: http://127.0.0.1:8000/
echo Press CTRL+C to stop the server
echo.

python manage.py runserver

pause

