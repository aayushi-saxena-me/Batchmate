# Fix: Django System Checks Error During Deployment

## The Error

```
File "/usr/local/lib/python3.12/site-packages/django/core/checks/registry.py", line 89, in run_checks
    new_errors = check(app_configs=app_configs, databases=databases)
```

This happens when Django runs system checks and something fails (usually database connection or validation).

---

## Root Causes & Solutions

### Cause 1: Wrong Settings Module (Most Likely)

**Problem:** Your app is using `settings.py` (SQLite) instead of `settings_production.py` (PostgreSQL) in production.

**Check:** What settings file is being used?
- Railway might be using default `settings.py` which expects SQLite
- But you're using PostgreSQL in production

**Solution:** Make sure production uses production settings.

#### Option A: Set Environment Variable (Railway)

1. Railway Dashboard → Your web service → Variables
2. Add new variable:
   - **Name:** `DJANGO_SETTINGS_MODULE`
   - **Value:** `inventory_management.settings_production`
3. Redeploy

#### Option B: Update WSGI to Auto-Detect

Update `inventory_management/wsgi.py` to use production settings when `DATABASE_URL` exists:

```python
import os
from django.core.wsgi import get_wsgi_application

# Use production settings if DATABASE_URL is set (production environment)
if os.environ.get('DATABASE_URL'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

application = get_wsgi_application()
```

---

### Cause 2: Database Connection Failing During Checks

**Problem:** Django checks try to connect to database, but:
- Database isn't ready yet
- `DATABASE_URL` not set correctly
- Connection timeout

**Solution 1: Skip Checks During Migrations**

If this happens during `migrate`, skip checks:

```bash
python manage.py migrate --skip-checks
```

**Solution 2: Disable Database Checks Temporarily**

Add to `settings_production.py`:

```python
# Skip database system checks (use with caution)
DATABASES['default']['TEST'] = {
    'CHARSET': None,
    'COLLATION': None,
}

# Or disable specific checks
SILENCED_SYSTEM_CHECKS = [
    'models.E006',  # Fields must not conflict
]
```

**Better Solution:** Make database checks optional in `settings_production.py`:

```python
# Database - Use PostgreSQL in production
if dj_database_url and os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=False,  # Disable health checks if causing issues
        )
    }
```

---

### Cause 3: Tables Exist But Django Doesn't Know

**Problem:** You created tables manually, but Django's checks fail because:
- Migration state doesn't match reality
- Django tries to validate models against database
- Schema mismatch detected

**Solution:** Run migrations to sync Django with existing tables:

```bash
# Run migrations (Django will detect existing tables)
python manage.py migrate

# If checks still fail, skip them:
python manage.py migrate --skip-checks

# Then mark migrations as fake if needed:
python manage.py migrate --fake inventory 0001_initial
```

---

### Cause 4: Missing DATABASE_URL

**Problem:** `DATABASE_URL` environment variable not set, so Django tries SQLite (which fails in production).

**Solution:** 
1. Railway → Web service → Variables
2. Check `DATABASE_URL` exists
3. If missing, add it from PostgreSQL service variables

---

## Quick Fixes (Try These in Order)

### Fix 1: Update WSGI to Use Production Settings

Update `inventory_management/wsgi.py`:

```python
import os
from django.core.wsgi import get_wsgi_application

# Auto-detect production environment
if os.environ.get('DATABASE_URL') or os.environ.get('RAILWAY_ENVIRONMENT'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings_production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

application = get_wsgi_application()
```

### Fix 2: Run Migrations with Skip Checks

In Railway Shell:
```bash
python manage.py migrate --skip-checks
```

### Fix 3: Set Environment Variable

In Railway Variables:
- `DJANGO_SETTINGS_MODULE` = `inventory_management.settings_production`

### Fix 4: Make Database Checks Optional

Update `settings_production.py`:

```python
# Around line 36, change:
conn_health_checks=True,  # Change to False
```

---

## Debug Steps

### Step 1: Check What Settings Are Being Used

In Railway Shell:
```bash
python manage.py shell
```

```python
from django.conf import settings
print(settings.DATABASES)
print(settings.SECRET_KEY[:20])  # Should NOT be the insecure default
```

If you see SQLite config, you're using wrong settings file.

### Step 2: Check DATABASE_URL

```python
import os
print(os.environ.get('DATABASE_URL'))
```

Should show PostgreSQL connection string, not None.

### Step 3: Test Database Connection

```python
from django.db import connection
connection.ensure_connection()
print("Connected!")
```

---

## Complete Solution (Recommended)

1. **Update `wsgi.py`** to auto-detect production
2. **Set `DJANGO_SETTINGS_MODULE`** environment variable in Railway
3. **Run migrations** with `--skip-checks` if needed
4. **Verify** database connection works

---

## If Nothing Works

Temporarily disable system checks in `settings_production.py`:

```python
# At the bottom of settings_production.py
import logging
logger = logging.getLogger('django')

# Override check method to be more lenient
def skip_database_checks(*args, **kwargs):
    """Skip database-related system checks"""
    return []

# Monkey patch (use sparingly!)
from django.core.management.base import BaseCommand
original_check = BaseCommand.check

def patched_check(self, **kwargs):
    if 'databases' in kwargs:
        kwargs.pop('databases')  # Skip database checks
    return original_check(self, **kwargs)

BaseCommand.check = patched_check
```

**⚠️ Warning:** Only use this as a last resort. It's better to fix the root cause.

---

## Expected Behavior After Fix

- Deployments should complete without check errors
- Migrations should run successfully
- Application should start normally
- Health check should pass

