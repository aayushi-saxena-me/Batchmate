# Verify Your Railway Setup

## Your Current Configuration ✅

You have:
- **Pre-deploy command:** `python manage.py migrate`
- **Start command:** `bash start.sh`

This is **correct!** Here's what should happen:

1. Railway runs `python manage.py migrate` BEFORE deploying (pre-deploy)
2. Railway starts the app with `bash start.sh` (start command)

---

## Why Migrations Might Not Have Run

If the healthcheck still shows "no such table", possible reasons:

### 1. Pre-deploy Command Not Executing
- Check Railway deployment logs - look for migration output
- Pre-deploy commands run BEFORE the service starts
- Check if there are any errors in the build logs

### 2. Database Not Connected During Pre-deploy
- `DATABASE_URL` must be set BEFORE pre-deploy runs
- Verify `DATABASE_URL` is in your Variables tab

### 3. Pre-deploy Failed Silently
- Check the deployment logs for error messages
- Look for "Operations to perform" or migration messages

---

## How to Verify It's Working

### Check Deployment Logs:

1. Railway → "web" service → **Deployments** tab
2. Click on the **latest deployment**
3. Click **"Logs"** tab
4. Scroll to the **beginning** of the logs (pre-deploy runs first)
5. Look for:
   - `python manage.py migrate`
   - `Operations to perform:`
   - `Running migrations:`
   - `Applying inventory.0001_initial... OK`

---

## If Migrations Still Haven't Run

### Option 1: Run Manually Once
Even with pre-deploy set, you might need to run it manually the first time:

1. Open Railway Shell (Deployments → Latest → Shell)
2. Run: `python manage.py migrate`
3. This will create the tables

### Option 2: Check Pre-deploy Command Syntax
Make sure the pre-deploy command is exactly:
```
python manage.py migrate
```

Or if that doesn't work, try:
```
python manage.py migrate --noinput
```

### Option 3: Trigger a New Deployment
Sometimes pre-deploy only runs on new deployments:
- Make a small change (add a comment to a file)
- Push to GitHub
- Railway will redeploy and run pre-deploy

---

## Your Start Command (`bash start.sh`)

This is correct! Your `start.sh`:
- Handles PORT variable
- Starts gunicorn
- Everything looks good

---

## Quick Test

1. **Check if migrations ran:**
   - Look at deployment logs (beginning of logs)
   - Should see migration output

2. **If not in logs:**
   - Run manually once via Shell
   - Then pre-deploy should handle future migrations

3. **Verify after running:**
   - Check healthcheck: `/health/`
   - `database_tables` should show "healthy"

---

**Your setup is correct - we just need to make sure migrations actually run!**


