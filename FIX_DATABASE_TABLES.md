# Fix: Migrations Ran But Tables Still Missing

## The Problem:
Migrations ran successfully, but healthcheck still says "no such table: inventory_product"

## Possible Causes:

### 1. Migrations Ran on Wrong Database
Pre-deploy might have used a different DATABASE_URL than runtime.

### 2. App Needs Restart
Sometimes Django needs a restart to see new tables.

### 3. DATABASE_URL Not Set During Pre-deploy
Pre-deploy might have run before DATABASE_URL was available.

---

## Solution: Run Migrations Manually

Even though pre-deploy ran migrations, let's run them manually to ensure they apply:

1. **Open Railway Shell:**
   - Railway → "web" service → Deployments → Latest → Shell

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Check output:**
   - Should say "No migrations to apply" if already run
   - OR will apply any missing migrations

4. **If it says "No migrations to apply"** but tables still missing:
   ```bash
   python manage.py migrate --run-syncdb
   ```

---

## Verify Database Connection

Check if the app is connecting to the correct database:

1. **In Railway Shell, run:**
   ```bash
   python manage.py dbshell
   ```

2. **Then in the database shell:**
   ```sql
   .tables
   ```
   (for SQLite) or
   ```sql
   \dt
   ```
   (for PostgreSQL)

3. **Check if inventory tables exist:**
   - Should see: inventory_product, inventory_category, etc.

---

## Alternative: Check DATABASE_URL

1. **In Railway Shell:**
   ```bash
   python manage.py shell
   ```

2. **Then in Python shell:**
   ```python
   from django.conf import settings
   print(settings.DATABASES['default'])
   ```

3. **Verify it matches your postgres service DATABASE_URL**

---

## Quick Fix: Force Restart

Sometimes a service restart fixes it:

1. Railway → "web" service → Settings
2. Look for "Restart" button or redeploy
3. After restart, check healthcheck again

---

**Try running migrations manually first, then let me know what happens!**


