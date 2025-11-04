# How to Run Migrations in Railway

## Quick Steps

### Option 1: Using Railway Dashboard (Easiest)

1. **Go to Railway Dashboard**
   - Open https://railway.app
   - Login to your account
   - Click on your project

2. **Open Your Web Service**
   - Click on the web service (not the database)

3. **Open Shell/Command Runner**
   - Click **"Deployments"** tab at the top
   - Click on the **latest deployment** (most recent one)
   - Look for **"Shell"** or **"Run Command"** button
   - Click it

4. **Run Migrations**
   - In the shell/command prompt, type:
     ```bash
     python manage.py migrate
     ```
   - Press Enter
   - Wait for it to complete

5. **Verify Success**
   - You should see output like:
     ```
     Operations to perform:
       Apply all migrations: admin, auth, contenttypes, inventory, sessions
     Running migrations:
       Applying auth.0001_initial... OK
       Applying inventory.0001_initial... OK
       ...
     ```

6. **Create Superuser** (Optional, but recommended)
   - In the same shell, run:
     ```bash
     python manage.py createsuperuser
     ```
   - Enter username, email, password when prompted

### Option 2: Using Railway CLI

If you have Railway CLI installed:

```bash
# Login to Railway
railway login

# Link to your project (if not already linked)
railway link

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

---

## Visual Guide

### Step 1: Railway Dashboard
```
Railway Dashboard
  └─ Your Project
      └─ Web Service (click this)
```

### Step 2: Deployments Tab
```
Web Service Page
  ├─ Settings
  ├─ Variables
  ├─ Deployments ← Click this
  └─ Metrics
```

### Step 3: Latest Deployment
```
Deployments List
  ├─ Deployment #3 (latest) ← Click this
  ├─ Deployment #2
  └─ Deployment #1
```

### Step 4: Shell/Command
```
Deployment Details
  ├─ Logs
  ├─ Shell ← Click this
  └─ Settings
```

### Step 5: Run Command
```
Shell Terminal
  $ python manage.py migrate
  [wait for output...]
  $ python manage.py createsuperuser
  [enter credentials...]
```

---

## Troubleshooting

### "Shell" Button Not Available

**Alternative:** Use "Run Command" or "Terminal" tab

**Or:** Use Railway CLI (see Option 2 above)

### "Command not found: python"

Try:
```bash
python3 manage.py migrate
```

Or:
```bash
python3.12 manage.py migrate
```

### "No such file or directory: manage.py"

Make sure you're in the project root directory:
```bash
ls  # Should show manage.py, requirements.txt, etc.
pwd  # Check current directory
cd /app  # If needed (Railway's default)
```

### Migrations Run but Still Getting Error

1. **Check if migrations actually ran:**
   ```bash
   python manage.py showmigrations
   ```
   - Should show `[X]` for applied migrations

2. **Check database connection:**
   - Make sure `DATABASE_URL` is set in Railway Variables
   - Check that PostgreSQL service is running

3. **Try running migrations again:**
   ```bash
   python manage.py migrate --run-syncdb
   ```

### Still Getting "auth_user table does not exist"

This means migrations didn't run successfully. Check:

1. **Migration logs:**
   - Look at the output when you ran `migrate`
   - Check for any errors

2. **Database connection:**
   - Verify `DATABASE_URL` is correct
   - Check PostgreSQL service is running

3. **Try manually:**
   ```bash
   python manage.py migrate auth
   python manage.py migrate
   ```

---

## After Migrations Complete

### Test Your Fix

1. **Run the check script again:**
   ```bash
   railway run python check_and_fix_user.py
   ```
   - Should now work!

2. **Access Admin:**
   - Go to: `https://your-app.railway.app/admin/`
   - Login with your superuser credentials

3. **Verify Tables:**
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   print(f"Users: {User.objects.count()}")
   ```

---

## Prevention: Auto-Run Migrations

I've already updated your `Procfile` to automatically run migrations on every deployment:

```bash
release: python manage.py migrate --noinput
web: gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**This means:**
- ✅ Migrations will run automatically on future deployments
- ✅ No need to manually run migrations each time
- ✅ The `release` command runs before `web` starts

**To activate this:**
1. Commit and push your updated `Procfile`
2. Railway will redeploy
3. Migrations will run automatically

---

## Quick Checklist

- [ ] Go to Railway Dashboard
- [ ] Open web service
- [ ] Click "Deployments" tab
- [ ] Click latest deployment
- [ ] Click "Shell" or "Run Command"
- [ ] Run: `python manage.py migrate`
- [ ] Wait for success message
- [ ] (Optional) Run: `python manage.py createsuperuser`
- [ ] Test admin access: `https://your-app.railway.app/admin/`

---

## Summary

**The Error:** Migrations haven't been run in Railway

**The Fix:** Run `python manage.py migrate` in Railway shell

**Future Prevention:** Updated `Procfile` will auto-run migrations on deployment

**Next Steps:**
1. Run migrations in Railway (see steps above)
2. Create superuser
3. Test admin access
4. Push updated `Procfile` to prevent future issues

