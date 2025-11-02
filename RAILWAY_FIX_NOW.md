# Fix Railway Right Now - Step by Step

## Current Situation:
- ✅ You have web service
- ✅ You have postgres database
- ❌ Web service is crashing (PORT error)
- ❌ Database not connected (need to add variable)

Let's fix both!

---

## Fix 1: Fix the PORT Error (Stop the Crash)

### Steps:

1. **In Railway, click on your "web" service** (not postgres)

2. **Click "Settings" tab** (at the top)

3. **Scroll down to find "Deploy" section**

4. **Look for "Start Command" field**

5. **Replace whatever is there with this:**
   ```
   gunicorn inventory_management.wsgi:application --bind 0.0.0.0:8000
   ```

6. **Click "Save" or the checkmark** (if there is one)

7. **Railway will automatically redeploy** - wait for it (2-3 minutes)

**✅ After this, your service should stop crashing!**

---

## Fix 2: Connect the Database

### Steps:

1. **Click on your "postgres" service** (the database, not web)

2. **Click "Variables" tab**

3. **Look for a variable called:**
   - `DATABASE_URL` 
   - OR `POSTGRES_URL`
   - OR `PGDATABASE`

4. **Click on it to see its value, OR copy the connection string**

5. **Now go back to your "web" service**

6. **Click "Variables" tab**

7. **Click "New Variable"**

8. **Add:**
   - **Name:** `DATABASE_URL`
   - **Value:** Paste the connection string from step 4
   - Click "Add"

**✅ Database is now connected!**

---

## Fix 3: Add Missing Variables

Still in "web" service → "Variables" tab:

### Add SECRET_KEY:
1. Click "New Variable"
2. **Name:** `SECRET_KEY`
3. **Value:** `ahi5c_@gstnuodxpabudwf&!%=p(n21id=30y8t=^ahgt6yrl5`
4. Click "Add"

### Add DEBUG:
1. Click "New Variable"
2. **Name:** `DEBUG`
3. **Value:** `False`
4. Click "Add"

### Add ALLOWED_HOSTS:
1. Click "New Variable"
2. **Name:** `ALLOWED_HOSTS`
3. **Value:** `*.railway.app`
4. Click "Add"

---

## After All Fixes:

1. **Wait for Railway to redeploy** (watch the Deployments tab)
2. **Check if service is running** (should show "Active" not "Crashed")
3. **Get your app URL:**
   - Web service → Settings tab → Scroll to "Domains"
   - Copy the URL (something like `https://xxx.railway.app`)

---

## Next: Run Migrations

Once service is running, we'll run migrations to set up the database tables.

---

## Quick Checklist:

- [ ] Fixed Start Command (Fix 1)
- [ ] Added DATABASE_URL variable (Fix 2)
- [ ] Added SECRET_KEY variable
- [ ] Added DEBUG variable
- [ ] Added ALLOWED_HOSTS variable
- [ ] Service is running (not crashing)
- [ ] Got app URL

---

**Tell me when you've done these fixes and we'll move to migrations!**

