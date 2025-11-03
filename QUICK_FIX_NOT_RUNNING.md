# Quick Fix: Application Not Running

## The Problem

Django is not installed in your current Python environment.

## The Solution

### Option 1: Use the Batch File (Easiest)

**Double-click or run:**
```cmd
start_app.bat
```

This will:
1. ✅ Create/activate virtual environment
2. ✅ Install all dependencies
3. ✅ Run migrations
4. ✅ Start the server

### Option 2: Manual Steps

**Step 1: Activate Virtual Environment**

In PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

If you get execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or use Command Prompt instead:
```cmd
venv\Scripts\activate
```

**Step 2: Install Dependencies**

```powershell
pip install -r requirements.txt
```

**Step 3: Run Migrations**

```powershell
python manage.py migrate
```

**Step 4: Start Server**

```powershell
python manage.py runserver
```

---

## How to Know It's Working

After running the server, you should see:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Then open your browser to: **http://127.0.0.1:8000/**

---

## If You Still Get Errors

### "Django not found" after installing
- Make sure virtual environment is activated (you should see `(venv)` in your prompt)
- Run: `pip install -r requirements.txt` again

### "Port already in use"
- Another process is using port 8000
- Use different port: `python manage.py runserver 8001`

### "No module named 'inventory'"
- Make sure you're in the project directory
- Check: `dir manage.py` should show the file

---

## Quick Test

Once server is running:

1. Open: http://127.0.0.1:8000/health/
   - Should show JSON response

2. Open: http://127.0.0.1:8000/accounts/login/
   - Should show login page

---

## Still Having Issues?

1. Check Python version: `python --version` (should be 3.8+)
2. Check if venv is activated: `python -c "import sys; print(sys.executable)"` (should show venv path)
3. Check Django: `python -c "import django; print(django.get_version())"`

See `START_APPLICATION.md` for detailed troubleshooting.

