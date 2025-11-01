# Running Migrations on Railway - Step by Step

## Method 1: Using Railway Dashboard (Easiest - Recommended) ✅

### Step-by-Step:

1. **Open Railway Dashboard**
   - Go to [railway.app](https://railway.app)
   - Login to your account
   - Select your project

2. **Navigate to Your Service**
   - Click on your **web service** (not the database, the Django app service)

3. **Open the Deployments Tab**
   - Click on **"Deployments"** tab at the top
   - You should see your deployment(s) listed

4. **Access the Shell/Console**
   - Click on the **latest deployment** (the most recent one)
   - Look for a button that says **"Shell"**, **"Console"**, **"Run Command"**, or **"..."** (three dots menu)
   - Click it to open a terminal

5. **Run Migrations**
   Once the shell/console opens, type:
   ```bash
   python manage.py migrate
   ```
   Press Enter and wait for it to complete.

6. **Create Superuser** (Optional but Recommended)
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts:
   - Username: (choose a username)
   - Email: (your email - can be blank)
   - Password: (create a strong password)

---

## Method 2: Using Railway CLI (For Advanced Users)

### Step 1: Install Railway CLI

**Windows (PowerShell):**
```powershell
# Option 1: Using npm (if you have Node.js)
npm i -g @railway/cli

# Option 2: Using Scoop (if you have Scoop)
scoop install railway

# Option 3: Using winget
winget install Railway.CLI
```

**Or download from:** https://github.com/railwayapp/cli/releases

### Step 2: Login to Railway
```bash
railway login
```
This will open your browser to authorize.

### Step 3: Link to Your Project
```bash
# Navigate to your project directory (if not already there)
cd "C:\Z Documents\Kids\Aayushi\Batchmate"

# Link to your Railway project
railway link
```
Select your project when prompted.

### Step 4: Run Migrations
```bash
railway run python manage.py migrate
```

### Step 5: Create Superuser
```bash
railway run python manage.py createsuperuser
```

---

## Method 3: Using Railway's One-Click Script (If Available)

Some Railway setups allow you to add a command in the deployment settings:

1. Go to your **service** → **Settings**
2. Look for **"Deploy"** or **"Build & Deploy"** section
3. Find **"Start Command"** or add a custom script
4. You can modify the start command, but this is not recommended for migrations

**Note:** Migrations should be run manually or via a deployment hook, not in the start command.

---

## Method 4: Using Railway Deploy Hooks (Advanced)

You can configure Railway to automatically run migrations on each deploy by modifying your `railway.json` or using a custom build script.

### Option A: Create a startup script

Create a file `railway-start.sh`:

```bash
#!/bin/bash
python manage.py migrate
gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT
```

Then set this as your start command in Railway settings.

### Option B: Modify railway.json

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python manage.py migrate && gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

---

## Troubleshooting

### "Command not found" or "python: command not found"
Try using `python3` instead:
```bash
python3 manage.py migrate
```

### "No module named django"
This means Django isn't installed. Check:
- Your `requirements.txt` includes Django
- Railway successfully installed dependencies (check build logs)

### "Database connection failed"
- Verify PostgreSQL service is running in Railway
- Check that `DATABASE_URL` environment variable is set
- In Railway: Your project → Database service → Variables tab → Check `DATABASE_URL`

### "Cannot find migrations"
Make sure you've committed your migration files to git:
```bash
git add inventory/migrations/
git commit -m "Add migrations"
git push
```

### Shell/Console button not visible
- Make sure you're looking at the **web service** (not database)
- Try clicking on the deployment itself, not just the service
- Some Railway plans might have different interfaces

---

## Recommended Approach

**For First Time Setup:**
1. Use **Method 1 (Dashboard)** - it's the easiest and most reliable
2. Run migrations once manually
3. Create your superuser

**For Ongoing Development:**
- Use **Method 1** when you add new migrations
- Or use **Method 2 (CLI)** if you prefer command line

**For Production:**
- Consider **Method 4** to automate migrations on deploy
- But always test migrations in a staging environment first!

---

## Quick Reference Commands

Once you're in Railway shell/console or using CLI:

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check migration status
python manage.py showmigrations

# Make new migrations (if needed, though usually done locally)
python manage.py makemigrations

# Check Django system
python manage.py check --deploy
```

---

## Visual Guide Locations in Railway

When looking for the Shell/Console in Railway Dashboard:

1. **Project Dashboard** → Your Service → **Deployments Tab**
2. Click on a **deployment** (the latest one)
3. Look for:
   - **"Shell"** button
   - **"Console"** button  
   - **"..."** (three dots) menu → "Open Shell"
   - **"Run Command"** option

The exact location may vary based on Railway's interface updates, but it's usually in the Deployments section.

---

**Pro Tip:** After running migrations successfully, you'll see output like:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, inventory, sessions
Running migrations:
  Applying inventory.0001_initial... OK
  ...
```

This confirms your migrations ran successfully! ✅

