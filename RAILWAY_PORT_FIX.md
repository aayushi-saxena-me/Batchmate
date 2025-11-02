# Fix: '$PORT' is not a valid port number

## The Problem
Railway is having trouble with the `$PORT` environment variable in your start command.

## Solution Options

### Solution 1: Use Nixpacks Builder (Easiest) ✅

I've updated your `railway.json` to use Nixpacks instead of Dockerfile. This is Railway's auto-detection builder and handles PORT automatically.

**What changed:**
- Changed builder from `DOCKERFILE` to `NIXPACKS`
- Railway will auto-detect Django and set up everything correctly

**Next steps:**
1. Commit and push the updated `railway.json`:
   ```bash
   git add railway.json
   git commit -m "Fix PORT issue - switch to Nixpacks"
   git push
   ```
2. Railway will automatically redeploy with the new configuration
3. The PORT issue should be resolved

### Solution 2: Fix Start Command in Railway Dashboard (Alternative)

If you prefer to keep using Dockerfile, fix it in Railway:

1. Go to your **web service** in Railway
2. Click **"Settings"** tab
3. Scroll to **"Deploy"** section
4. Find **"Start Command"** field
5. Change it to:
   ```
   gunicorn inventory_management.wsgi:application --bind 0.0.0.0:${PORT:-8000}
   ```
   OR simply:
   ```
   python manage.py migrate && gunicorn inventory_management.wsgi:application --bind 0.0.0.0:8000
   ```
6. Save changes
7. Railway will redeploy

### Solution 3: Use Environment Variable in Railway

1. In Railway dashboard → Your service → **Variables** tab
2. Add a new variable:
   - Name: `PORT`
   - Value: Leave it empty (Railway auto-sets this)
   - OR set to a specific port like `8000`
3. Make sure the start command uses `$PORT` or `${PORT}`

## Recommended: Use Solution 1 (Nixpacks)

Nixpacks is Railway's smart builder that:
- ✅ Auto-detects Django
- ✅ Handles PORT automatically
- ✅ Sets up Python environment correctly
- ✅ Less configuration needed

## After Fixing

1. Wait for Railway to redeploy
2. Check the logs to see if the service starts successfully
3. Once it's running, proceed with migrations

## Verify It's Working

After redeployment, check:
- Service status should be "Active" (not crashing)
- Logs should show "Listening on port..." or similar
- No PORT errors in the logs

---

**Quick Fix:** Commit the updated `railway.json` file and push to GitHub. Railway will automatically redeploy!

