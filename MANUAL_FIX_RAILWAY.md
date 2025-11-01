# Manual Fix for Railway - Do This Now

Since the automatic fixes aren't working, let's do it manually in Railway dashboard.

## Fix 1: Add PORT Variable (CRITICAL)

1. In Railway → Click "web" service
2. Click "Variables" tab
3. Click "New Variable"
4. Add:
   - **Name:** `PORT`
   - **Value:** `8000`
5. Click "Add"

This will fix the PORT error!

---

## Fix 2: Add DATABASE_URL (Connect Database)

1. Click "postgres" service
2. Variables tab → Copy the `DATABASE_URL` value (the entire connection string)
3. Go back to "web" service → Variables tab
4. Click "New Variable"
5. Add:
   - **Name:** `DATABASE_URL`
   - **Value:** Paste what you copied from postgres
6. Click "Add"

---

## Fix 3: Add Other Required Variables

Still in "web" service → Variables tab:

### SECRET_KEY
- Click "New Variable"
- **Name:** `SECRET_KEY`
- **Value:** `ahi5c_@gstnuodxpabudwf&!%=p(n21id=30y8t=^ahgt6yrl5`
- Click "Add"

### DEBUG
- Click "New Variable"
- **Name:** `DEBUG`
- **Value:** `False`
- Click "Add"

### ALLOWED_HOSTS
- Click "New Variable"
- **Name:** `ALLOWED_HOSTS`
- **Value:** `*.railway.app`
- Click "Add"

---

## After Adding All Variables

1. Railway will automatically restart/redeploy
2. Wait 2-3 minutes
3. Check service status - should be "Active" not "Crashing"
4. Check logs - should show "Listening on port 8000" or similar

---

## Your Variables Checklist

In "web" service Variables tab, you should have:
- [ ] `PORT` = `8000`
- [ ] `DATABASE_URL` = (connection string from postgres)
- [ ] `SECRET_KEY` = (the key I gave you)
- [ ] `DEBUG` = `False`
- [ ] `ALLOWED_HOSTS` = `*.railway.app`

---

**Do Fix 1 first (add PORT variable) - that should stop the crashing!**

Then add the others.

