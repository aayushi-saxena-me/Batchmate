# Manual Setup Instructions

Since automated installation isn't working in this environment, please follow these steps manually:

## Step 1: Install Dependencies

Open a **new** PowerShell or Command Prompt window and run:

```powershell
py -3.12 -m pip install django django-crispy-forms crispy-bootstrap5 Pillow
```

Or if that doesn't work, try:
```powershell
python -m pip install django django-crispy-forms crispy-bootstrap5 Pillow
```

**Wait for the installation to complete** (you should see packages being downloaded and installed).

## Step 2: Create Database Migrations

Navigate to the project folder and run:
```powershell
cd "C:\Z Documents\Kids\Aayushi\Batchmate"
py -3.12 manage.py makemigrations
```

Or:
```powershell
python manage.py makemigrations
```

## Step 3: Apply Migrations

```powershell
py -3.12 manage.py migrate
```

Or:
```powershell
python manage.py migrate
```

## Step 4: Create Admin User (Optional but Recommended)

```powershell
py -3.12 manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password (twice)

## Step 5: Start the Server

```powershell
py -3.12 manage.py runserver
```

Or:
```powershell
python manage.py runserver
```

## Step 6: Access the Application

Open your web browser and go to:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## Troubleshooting

### "No module named django"
- Make sure Step 1 completed successfully
- Try: `python -m pip list` to see if Django is installed
- If not installed, try: `python -m pip install --user django`

### "Command not found: py"
- Use `python` instead of `py -3.12`
- Or use `python3` if available

### Port 8000 already in use
- Use a different port: `python manage.py runserver 8001`
- Then access at: http://127.0.0.1:8001/

### Permission errors
- Try running PowerShell/Command Prompt as Administrator
- Or use: `python -m pip install --user django django-crispy-forms crispy-bootstrap5 Pillow`

---

## Quick Alternative: Use the Batch Files

I've created two batch files you can double-click:

1. **setup_and_run.bat** - Runs all setup steps
2. **run_server.bat** - Starts the server (after setup is complete)

Just double-click these files in Windows Explorer!

