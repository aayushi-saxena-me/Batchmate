# Fix: Server Error (500) on Login Page

## The Problem

You're seeing a **500 Internal Server Error** when accessing:
`https://web-production-cd1a5.up.railway.app/accounts/login/`

## Root Causes

The most common causes are:

### 1. **Database Connection Failing** ⚠️ (Most Likely)
- Django tries to check if user is authenticated
- This requires a database query
- If database connection fails → 500 error

### 2. **Auth Tables Don't Exist**
- `auth_user` table missing (migrations not run)
- Template tries to check `user.is_authenticated`
- Database query fails → 500 error

### 3. **Template Error**
- Missing template files
- Crispy forms not installed
- Static files not loading

---

## Quick Fixes (Try in Order)

### Fix 1: Run Auth Migrations

The `auth_user` table must exist for login to work:

```bash
python manage.py migrate auth
python manage.py migrate
```

This creates:
- `auth_user` table (stores user accounts)
- `auth_group`, `auth_permission`, etc.
- Other Django auth system tables

**Do this first!** Login requires the auth tables to exist.

### Fix 2: Check Database Connection

In Railway Shell:
```bash
python manage.py shell
```

```python
from django.db import connection
connection.ensure_connection()
print("Database connected!")
```

If this fails, your `DATABASE_URL` is wrong or database isn't accessible.

### Fix 3: Make Login View More Robust

Update `accounts/views.py` to handle database errors gracefully.

### Fix 4: Check Railway Logs

1. Railway Dashboard → Your web service → **Deployments** → Latest → **Logs**
2. Look for the actual error message
3. Share the traceback - it will tell us exactly what's failing

---

## Detailed Fix: Update Login View

Make the login view handle database errors:

```python
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db import connection
from django.db.utils import OperationalError

def login_view(request):
    """User login view with error handling"""
    # Try to check authentication, but don't fail if database is down
    try:
        is_authenticated = request.user.is_authenticated
    except Exception:
        # If database check fails, assume not authenticated
        is_authenticated = False
    
    if is_authenticated:
        return redirect('inventory:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('inventory:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})
```

---

## Most Likely Solution

**Run migrations first!**

```bash
# In Railway Shell or locally:
python manage.py migrate auth      # Creates auth_user table
python manage.py migrate            # Applies all migrations
```

The login page requires the `auth_user` table to exist. Without it, Django can't even check if a user is authenticated, causing the 500 error.

---

## Check What's Actually Wrong

### Step 1: Check Railway Logs

The logs will show the exact error. Look for:
- `OperationalError` → Database connection issue
- `DoesNotExist` → Table missing
- `TemplateDoesNotExist` → Template issue
- `ImportError` → Missing package

### Step 2: Test Database Connection

```bash
python manage.py dbshell
```

If this works, database is accessible. Then check tables:
```sql
\dt  -- List all tables (PostgreSQL)
```

Should see `auth_user` table.

### Step 3: Test Auth Tables

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
User.objects.count()  # Should work if auth_user exists
```

If this fails, run `python manage.py migrate auth`.

---

## Complete Fix Sequence

1. **Run auth migrations:**
   ```bash
   python manage.py migrate auth
   ```

2. **Run all migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Verify auth_user exists:**
   ```bash
   python manage.py dbshell
   ```
   Then: `\dt` (should see `auth_user`)

4. **Try login page again**

5. **If still failing, check logs** for the exact error

---

## Expected Result

After running migrations:
- ✅ `auth_user` table exists
- ✅ Login page loads without 500 error
- ✅ You can create users with `python manage.py createsuperuser`
- ✅ Users can log in

---

## If Still Not Working

1. **Check Railway logs** - they'll show the exact error
2. **Verify DATABASE_URL** is set correctly
3. **Check if database service is running** in Railway
4. **Share the error traceback** from logs - that will tell us exactly what's wrong

