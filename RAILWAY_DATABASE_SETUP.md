# Railway Database Connection Setup

## Current Issue: Database Not Connected

You're seeing "Trying to connect a database? Add Variable" which means your web service needs the `DATABASE_URL` environment variable.

## Solution: Two Methods

### Method 1: Auto-Connect (Easiest) ✅

1. **Go back to your Project Dashboard**
   - Click your project name at the top
   - You should see all your services listed

2. **Check if PostgreSQL Database Service Exists**
   - Look for a service with PostgreSQL icon or named "Postgres" or "PostgreSQL"
   - If you DON'T see one, you need to create it first (see below)

3. **If Database Service Exists:**
   - Click on the **database service** (PostgreSQL)
   - Go to **"Variables"** tab
   - Look for `DATABASE_URL` or `POSTGRES_URL`
   - Copy this entire connection string

4. **Back to Web Service:**
   - Go back to your **web service** (Django app)
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - Name: `DATABASE_URL`
   - Value: Paste the connection string you copied
   - Click **"Add"**

### Method 2: Create Database Service (If It Doesn't Exist)

1. **In Project Dashboard:**
   - Click **"New"** button (usually top right)
   - Select **"Database"**
   - Choose **"Add PostgreSQL"**
   - Railway will automatically create it

2. **Railway Auto-Connects:**
   - Railway should automatically add `DATABASE_URL` to your web service
   - But if it doesn't, use Method 1 above

### Method 3: Railway's Auto-Variable Feature

Railway has a feature to automatically link databases. When you create a PostgreSQL service:
- Railway usually automatically creates `DATABASE_URL` in connected services
- But sometimes you need to manually link them

**To check if it's already linked:**
- In your web service Variables tab
- Look for `DATABASE_URL` in the existing variables list
- If it exists, you're good! ✅
- If not, use Method 1 to add it manually

## After Database is Connected

Once `DATABASE_URL` is set in your web service variables:

1. The web service will automatically restart
2. Then you can run migrations (next step!)

## Quick Checklist

- [ ] PostgreSQL database service exists in your project
- [ ] `DATABASE_URL` variable exists in web service Variables tab
- [ ] Database is connected (Railway shows connection status)

---

**Next Step After Database is Connected:** Run migrations using the Shell!

