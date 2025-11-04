# Debug: Railway Environment Variables Not Working

## The Issue

You see `DJANGO_SUPERUSER_USERNAME=admin` set in Railway, but the script says it's not set.

## Possible Causes

### 1. Variable Not Available During Release Phase

Railway's `release` command runs **before** environment variables might be fully loaded in some cases.

**Solution:** Try moving to a different phase or ensuring variables are set before deployment.

### 2. Variable Set in Wrong Service

Make sure the variable is set in the **web service**, not the database service.

**Check:**
- Railway Dashboard → Your **web service** (not database)
- Variables tab
- Should see `DJANGO_SUPERUSER_USERNAME` there

### 3. Variable Name Typo

Check for:
- Extra spaces
- Case sensitivity
- Exact spelling: `DJANGO_SUPERUSER_USERNAME` (all caps, underscores)

### 4. Variable Scope

Railway has different variable scopes:
- **Service-level** (recommended)
- **Project-level** (might not be available to all services)

**Fix:** Set variables at the **service level** (web service).

## Debugging Steps

### Step 1: Check What Script Actually Sees

The updated script now prints what it sees. Check deployment logs for:

```
🔍 Debug: Checking environment variables...
   Found Django/Superuser variables:
     DJANGO_SUPERUSER_USERNAME = 'admin'
     ...
```

This will show what Railway is actually passing to the script.

### Step 2: Verify Variable in Railway

1. **Go to Railway Dashboard**
2. **Click your web service** (not database)
3. **Click "Variables" tab**
4. **Verify:**
   - Variable name: `DJANGO_SUPERUSER_USERNAME` (exact spelling)
   - Variable value: `admin` (not `"admin"` with quotes)
   - No extra spaces

### Step 3: Check Variable Scope

In Railway Variables:
- Make sure it's set for the **web service** (not project-wide only)
- Check if there are multiple services - variable should be on the web service

### Step 4: Try Manual Test

In Railway shell, test if variable is available:

```bash
echo $DJANGO_SUPERUSER_USERNAME
```

Should print: `admin`

If it's empty, the variable isn't being loaded.

## Alternative: Use Railway CLI

Set variables via CLI to ensure they're set correctly:

```bash
railway variables set DJANGO_SUPERUSER_USERNAME=admin
railway variables set DJANGO_SUPERUSER_PASSWORD=your_password
railway variables set DJANGO_SUPERUSER_EMAIL=admin@example.com
```

## Updated Script

The script now:
1. ✅ **Prints all environment variables** (for debugging)
2. ✅ **Shows what values it's reading**
3. ✅ **Shows length of values** (to detect empty strings)
4. ✅ **Exits gracefully** instead of crashing

## What to Look For in Logs

After deploying, check logs for:

```
🔍 Debug: Checking environment variables...
   Found Django/Superuser variables:
     DJANGO_SUPERUSER_USERNAME = 'admin'
     DJANGO_SUPERUSER_PASSWORD = '********'
     DJANGO_SUPERUSER_EMAIL = 'admin@example.com'

📋 Values read:
   Username: 'admin' (length: 5)
   Email: 'admin@example.com' (length: 18)
   Password: ******** (length: 12)
```

If you see:
- `No DJANGO_SUPERUSER_* variables found` → Variables aren't being loaded
- `Username: '' (length: 0)` → Variable is empty
- `Username: 'your_username'` → Placeholder value

## Quick Fix

1. **Check deployment logs** - Look for the debug output
2. **Verify variable spelling** - Must be exactly `DJANGO_SUPERUSER_USERNAME`
3. **Check service** - Must be on web service, not database
4. **Redeploy** - After fixing variables, trigger a new deployment

## If Still Not Working

Try this workaround - set variables in a different way:

### Option 1: Use railway.json

```json
{
  "deploy": {
    "startCommand": "python manage.py migrate --noinput && python create_superuser_from_env.py || true && gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT"
  }
}
```

### Option 2: Create Superuser Manually

Skip auto-creation and create manually:

1. Remove variables from Railway
2. In Railway shell:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter credentials when prompted

## Summary

**Most Likely Issue:**
- Variable set in wrong service (database instead of web)
- Variable not available during `release` phase
- Variable name has typo

**Next Steps:**
1. Check deployment logs for debug output
2. Verify variable is on web service (not database)
3. Check exact spelling: `DJANGO_SUPERUSER_USERNAME`
4. Redeploy after fixing

The debug output will tell us exactly what's happening!

