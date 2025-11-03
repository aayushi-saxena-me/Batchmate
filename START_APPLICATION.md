# How to Start the Application

## Problem: Application Not Running

The issue is that **Django is not installed** in your current Python environment.

## Solution: Activate Virtual Environment and Install Dependencies

### Option 1: Use Existing Virtual Environment (Recommended)

I see you have virtual environments in your project. Let's activate one:

**For Windows PowerShell:**
```powershell
# Try venv first
.\venv\Scripts\Activate.ps1

# If that doesn't work, try:
.\venv312\Scripts\Activate.ps1
```

**For Windows Command Prompt (cmd):**
```cmd
venv\Scripts\activate
```

**For Git Bash:**
```bash
source venv/Scripts/activate
```

### Option 2: Create New Virtual Environment

If existing venvs don't work, create a new one:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1
```

### Step 2: Install Dependencies

Once virtual environment is activated, install packages:

```powershell
pip install -r requirements.txt
```

This will install:
- Django
- django-crispy-forms
- Pillow
- And other dependencies

### Step 3: Verify Django is Installed

```powershell
python -c "import django; print('Django version:', django.get_version())"
```

Should show: `Django version: 4.2.x` (or similar)

### Step 4: Run Migrations (if needed)

```powershell
python manage.py migrate
```

### Step 5: Start the Server

```powershell
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

---

## Quick Start Script

I'll create a batch file to automate this. But first, let's try the manual steps above.

---

## Troubleshooting

### "Execution Policy" Error in PowerShell

If you get an execution policy error when activating venv:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### "No module named 'django'" Error

This means:
1. Virtual environment is not activated, OR
2. Django is not installed

**Fix:**
```powershell
# Make sure venv is activated (you should see (venv) in prompt)
pip install -r requirements.txt
```

### "Port already in use" Error

If port 8000 is busy:
```powershell
python manage.py runserver 8001
```

Then access at: `http://127.0.0.1:8001/`

---

## Check Current Status

Run these commands to diagnose:

```powershell
# Check if venv is activated (should show venv path)
python -c "import sys; print(sys.executable)"

# Check if Django is installed
python -c "import django; print('Django:', django.get_version())"

# Check if you're in the right directory
pwd
```

---

## Next Steps After Server Starts

1. **Open browser:** http://127.0.0.1:8000/
2. **Health check:** http://127.0.0.1:8000/health/
3. **Register/Login:** http://127.0.0.1:8000/accounts/login/

See `BROWSER_TESTING_URLS.md` for all available URLs.

