# Fix: Connection Refused Error

The "connection refused" error means Railway can't reach your app. Let's troubleshoot:

---

## Step 1: Check Service Status

1. In Railway → Click **"web"** service
2. Look at the **top of the page** - what does it say?
   - "Active" ✅ (good - service is running)
   - "Crashed" ❌ (service keeps crashing)
   - "Building" ⏳ (still deploying)

**What do you see?**

---

## Step 2: Check Logs

1. In Railway → **"web"** service
2. Click **"Deployments"** tab
3. Click on the **latest deployment**
4. Click **"Logs"** tab
5. Scroll to the **bottom** (most recent logs)

**Look for:**
- ✅ "Listening on..." or "Starting gunicorn" = App is starting
- ❌ Error messages = Something is wrong
- ❌ Database connection errors
- ❌ Import errors
- ❌ "No module named..." errors

**What do the logs show? Copy the last few lines of error messages if any.**

---

## Step 3: Common Issues

### Issue A: Service is Crashing

If service shows "Crashed", check logs for:
- **Database connection error** → Need to add DATABASE_URL
- **Missing environment variable** → Need to add SECRET_KEY, etc.
- **Import errors** → Missing dependencies
- **Port binding errors** → Port configuration issue

### Issue B: Service Shows "Active" but Still Getting Connection Refused

This might mean:
- App started but then crashed immediately
- Port mismatch (Railway expects different port)
- Check logs for runtime errors

---

## Step 4: Quick Fixes to Try

### Fix 1: Verify All Environment Variables Are Set

In "web" service → Variables tab, make sure you have:
- [ ] `DATABASE_URL` (from postgres service)
- [ ] `SECRET_KEY`
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS=*.railway.app`
- [ ] `PORT=8000` (if not using fixed port)

### Fix 2: Restart the Service

1. In Railway → "web" service
2. Click **"Settings"** tab
3. Look for **"Restart"** or **"Redeploy"** button
4. Click it to restart the service

### Fix 3: Check Start Command

1. "web" service → **Settings** tab
2. Scroll to **"Deploy"** section
3. Check **"Start Command"** - should be:
   ```
   gunicorn inventory_management.wsgi:application --bind 0.0.0.0:8000
   ```
4. If it's different, Railway might be overriding it

---

## What to Check First:

1. **Service Status** - Is it "Active", "Crashed", or "Building"?
2. **Recent Logs** - What errors do you see at the bottom?
3. **Environment Variables** - Are they all set?

**Tell me what you find and we'll fix it!**

