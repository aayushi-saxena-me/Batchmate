# Fix: "no such table: auth_user" in Deployment

## The Problem

You're getting this error in deployment:
```
sqlite3.OperationalError: no such table: auth_user
```

This means **Django migrations haven't been run** in your deployment environment.

## The Solution

Run migrations in your deployment environment. Here's how for each platform:

---

## Railway.app

### Option 1: Using Railway Dashboard (Easiest)

1. **Go to Railway Dashboard**
   - Open your project
   - Click on your web service

2. **Run Migrations**
   - Click **"Deployments"** tab
   - Click on the latest deployment
   - Click **"Shell"** or **"Run Command"**
   - Enter: `python manage.py migrate`
   - Click **"Run"**

3. **Create Superuser** (after migrations)
   - In the same shell, run: `python manage.py createsuperuser`
   - Enter username, email, password

### Option 2: Using Railway CLI

```bash
# Login to Railway
railway login

# Link to your project
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

---

## Render.com

### Using Render Dashboard

1. **Go to Render Dashboard**
   - Open your web service
   - Click **"Shell"** tab

2. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

3. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

---

## Fly.io

### Using Fly CLI

```bash
# SSH into your app
fly ssh console

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Exit
exit
```

Or in one command:
```bash
fly ssh console -C "python manage.py migrate && python manage.py createsuperuser"
```

---

## Make Migrations Run Automatically

To prevent this in the future, you can add migrations to your startup script:

### Option 1: Update Procfile

```bash
release: python manage.py migrate
web: gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Note:** The `release` command runs before `web` starts (supported by Railway, Render, Heroku).

### Option 2: Update start.sh

```bash
#!/bin/bash
set -e

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Use PORT if set by Railway, otherwise default to 8000
PORT=${PORT:-8000}

# Start gunicorn
exec gunicorn inventory_management.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

### Option 3: Update Railway.json

If using Railway, add a build command:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## Step-by-Step Fix (Railway Example)

### Step 1: Run Migrations

1. Go to Railway Dashboard
2. Click your web service
3. Click **"Deployments"** tab
4. Click latest deployment
5. Click **"Shell"** or **"Run Command"**
6. Run: `python manage.py migrate`

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, inventory, sessions
Running migrations:
  Applying auth.0001_initial... OK
  Applying inventory.0001_initial... OK
  ...
```

### Step 2: Create Superuser

In the same shell:
```bash
python manage.py createsuperuser
```

Enter:
- Username
- Email
- Password

### Step 3: Verify

1. Go to your app URL: `https://your-app.railway.app/admin/`
2. Login with your superuser credentials
3. Should work now!

---

## Quick Fix Script

I've updated `check_and_fix_user.py` to detect this error and provide helpful instructions.

**After running migrations**, you can use:
```bash
railway run python check_and_fix_user.py
```

---

## Prevention: Auto-Run Migrations

### Recommended: Update Procfile

```bash
release: python manage.py migrate --noinput
web: gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

This will:
- ✅ Run migrations automatically on every deployment
- ✅ Use `--noinput` to skip prompts (necessary in deployment)
- ✅ Run before the web server starts

---

## Summary

**The Error:**
- `no such table: auth_user` = Migrations haven't been run

**The Fix:**
1. Run `python manage.py migrate` in deployment
2. Create superuser with `python manage.py createsuperuser`
3. (Optional) Add migrations to startup script to prevent future issues

**Platform-Specific:**
- **Railway:** Dashboard → Deployments → Shell → `python manage.py migrate`
- **Render:** Dashboard → Shell → `python manage.py migrate`
- **Fly.io:** `fly ssh console -C "python manage.py migrate"`

After running migrations, your `check_and_fix_user.py` script should work!

