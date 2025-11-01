# Railway.app Deployment - Step-by-Step Guide

## 🎯 Your Generated SECRET_KEY
**IMPORTANT:** Save this key - you'll need it in step 4!

```
ahi5c_@gstnuodxpabudwf&!%=p(n21id=30y8t=^ahgt6yrl5
```

**Never commit this to git!** It will be added as an environment variable in Railway.

---

## Step 1: Prepare Your Code ✅

Your code is already on GitHub! You're ready to deploy.

---

## Step 2: Sign Up / Login to Railway

1. Go to **[railway.app](https://railway.app)**
2. Click **"Login"** or **"Start a New Project"**
3. Choose **"Login with GitHub"**
4. Authorize Railway to access your GitHub repositories

---

## Step 3: Create New Project from GitHub

1. After logging in, click the **"+"** button or **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: **Batchmate** (or whatever your repo is named)
4. Railway will automatically detect it's a Django app

---

## Step 4: Configure Environment Variables

1. In your Railway project, click on your **service** (the web service)
2. Go to the **"Variables"** tab
3. Click **"New Variable"** and add these one by one:

### Required Variables:

| Variable Name | Value | Notes |
|--------------|-------|-------|
| `SECRET_KEY` | `ahi5c_@gstnuodxpabudwf&!%=p(n21id=30y8t=^ahgt6yrl5` | The key we just generated |
| `DEBUG` | `False` | Must be False for production |
| `ALLOWED_HOSTS` | `*.railway.app` | Will be your app's domain |

**To add each variable:**
- Click "New Variable"
- Enter the variable name (e.g., `SECRET_KEY`)
- Enter the value
- Click "Add"

---

## Step 5: Add PostgreSQL Database

1. In your Railway project dashboard, click **"New"** button
2. Select **"Database"**
3. Choose **"Add PostgreSQL"**
4. Railway will automatically:
   - Create the database
   - Set the `DATABASE_URL` environment variable
   - Your app will automatically connect to it!

---

## Step 6: Configure the Service

Railway should auto-detect your Django app, but let's verify:

1. Click on your **web service**
2. Go to **"Settings"** tab
3. Check the following:

**Build Command** (should be auto-detected):
```
pip install -r requirements.txt
```

**Start Command:**
```
gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT
```

**Note:** Railway automatically sets the `$PORT` variable.

---

## Step 7: Deploy!

1. Railway will automatically deploy when you connect the repo
2. If not auto-deploying, click **"Deploy"** button
3. Watch the build logs - it should show:
   - Installing dependencies
   - Collecting static files
   - Starting the server

**First deployment takes 3-5 minutes.**

---

## Step 8: Run Database Migrations

After your first deployment completes:

### Option A: Using Railway Dashboard (Easiest)

1. Click on your **service**
2. Go to **"Deployments"** tab
3. Click on the latest deployment
4. Click **"View Logs"**
5. Click the **"Shell"** button (or find "Run Command")
6. Run:
   ```bash
   python manage.py migrate
   ```
7. Then create superuser:
   ```bash
   python manage.py createsuperuser
   ```
   (Follow the prompts to create your admin account)

### Option B: Using Railway CLI (Advanced)

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login:
   ```bash
   railway login
   ```

3. Link to your project:
   ```bash
   railway link
   ```

4. Run migrations:
   ```bash
   railway run python manage.py migrate
   railway run python manage.py createsuperuser
   ```

---

## Step 9: Access Your App! 🎉

1. In Railway dashboard, click your **service**
2. Go to **"Settings"** tab
3. Scroll to **"Domains"** section
4. You'll see a URL like: `https://your-app-name.railway.app`
5. Click the link or copy it!

**Your app is now live!** ✨

---

## Step 10: Create Your Admin Account

1. Visit: `https://your-app-name.railway.app/admin`
2. Login with the superuser credentials you created in Step 8
3. Or create a regular user account at: `https://your-app-name.railway.app/accounts/register/`

---

## Troubleshooting

### Build Fails
- Check the build logs in Railway dashboard
- Verify `requirements.txt` has all dependencies
- Ensure `Dockerfile` is correct (if using)

### Database Connection Error
- Verify PostgreSQL service is running
- Check that `DATABASE_URL` is set automatically
- In Variables tab, verify `DATABASE_URL` exists

### Static Files Not Loading
- Railway should auto-collect static files during build
- If not, add to build command: `python manage.py collectstatic --noinput`

### 500 Error After Deployment
- Check logs in Railway dashboard
- Verify `DEBUG=False` and `SECRET_KEY` are set
- Check `ALLOWED_HOSTS` includes your Railway domain

### Can't Access Admin Panel
- Make sure you ran migrations and created superuser
- Check that you're using the correct URL

---

## Quick Commands Reference

```bash
# View logs
# (In Railway dashboard → Service → Deployments → View Logs)

# Run migrations (via Shell/CLI)
python manage.py migrate

# Create superuser (via Shell/CLI)
python manage.py createsuperuser

# Check Django system
python manage.py check --deploy
```

---

## What's Next?

After successful deployment:

1. ✅ Test your app at the Railway URL
2. ✅ Login and create test data
3. ✅ Customize domain (optional - Railway allows custom domains)
4. ✅ Set up monitoring (Railway has built-in metrics)
5. ✅ Configure backups for database (Railway → Database → Settings)

---

## Cost

Railway provides **$5/month free credit**, which is usually enough for:
- 1 web service
- 1 PostgreSQL database (small)
- Moderate traffic

You'll only be charged if you exceed the free credit. Monitor usage in Railway dashboard.

---

**Need help?** Check Railway's docs: https://docs.railway.app

