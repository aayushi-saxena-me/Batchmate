# Railway Port Routing Issue - Solution

## The Problem:
- Using `$PORT` → Service crashes (PORT not set or invalid)
- Using hardcoded `8000` → App runs but "connection refused" (Railway routing mismatch)

## Root Cause:
Railway's edge network expects the app to listen on the port Railway provides via `$PORT`, but when `$PORT` isn't properly set or read, the app crashes. When we hardcode 8000, the app runs but Railway routes to a different port.

## Solution Applied:
Updated `railway.json` to use `${PORT:-8000}` which means:
- Use `$PORT` if it's set
- Fall back to 8000 if `$PORT` is not set

This should handle both scenarios.

---

## Alternative: Check Railway Service Settings

If this still doesn't work, check Railway's port configuration:

1. In Railway → "web" service → **Settings** tab
2. Look for **"Network"** or **"Port"** section
3. Check if there's a port configuration option
4. Railway might expect you to expose/configure the port

---

## Another Option: Remove PORT Variable

Try removing the `PORT=8000` variable from Railway and let Railway auto-set it:

1. "web" service → Variables tab
2. Find `PORT` variable
3. Delete it
4. Railway will auto-assign a port and set `$PORT`
5. Redeploy

This might help Railway properly set the PORT variable.

---

## Check Railway's Expected Port

1. "web" service → **Settings** tab
2. Look for **"Domains"** or **"Networking"** section
3. Check if there's a port mentioned
4. Railway might be routing to a specific port that we need to match

---

**Try the updated code first (with fallback), then if it still crashes, try removing the PORT variable and letting Railway auto-set it.**

