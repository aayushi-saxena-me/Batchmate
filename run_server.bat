@echo off
echo Starting Django Development Server...
echo.

REM Try to find Python executable (prefer Anaconda)
set PYTHON_CMD=
if exist "C:\Users\gtg09\anaconda3\python.exe" (
    set PYTHON_CMD=C:\Users\gtg09\anaconda3\python.exe
) else (
    where py >nul 2>&1
    if %errorlevel% == 0 (
        set PYTHON_CMD=py -3.12
    ) else (
        where python >nul 2>&1
        if %errorlevel% == 0 (
            set PYTHON_CMD=python
        ) else (
            echo ERROR: Python not found!
            pause
            exit /b 1
        )
    )
)

echo Using: %PYTHON_CMD%
echo.
echo Open your browser to: http://127.0.0.1:8000
echo Press Ctrl+C to stop the server
echo.
%PYTHON_CMD% manage.py runserver

