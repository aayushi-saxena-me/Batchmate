# How to Run Migrations and Create Admin User

## Running Migrations

Migrations are **separate** from creating an admin user. Here's how to do both:

### Step 1: Run Migrations

**For Local Development (Windows):**
```powershell
python manage.py migrate
```

**For Production/Server (Railway/Render/etc.):**
```bash
python manage.py migrate
```

Or if using Railway CLI:
```bash
railway run python manage.py migrate
```

### What Migrations Do:
- ✅ Detects existing tables (like the ones you created manually)
- ✅ Creates any missing tables
- ✅ Updates Django's migration tracking (`django_migrations` table)
- ✅ Ensures database schema matches your models

**Important:** Even if you created tables manually, you should still run migrations. Django will detect them and mark migrations as applied.

---

## Step 2: Create Admin User (Separate Step)

Creating an admin user is **NOT part of migrations** - it's a separate command.

### Create Admin User Locally:
```powershell
python manage.py createsuperuser
```

You'll be prompted to enter:
1. **Username** - Choose a username (e.g., `admin`)
2. **Email** - Optional, but recommended
3. **Password** - Enter password (twice for confirmation)

### Create Admin User on Server:

**Option 1: Using Railway Shell:**
1. Railway Dashboard → Your web service → Deployments → Latest → Shell
2. Run:
   ```bash
   python manage.py createsuperuser
   ```
3. Follow prompts (same as above)

**Option 2: Using Railway CLI:**
```bash
railway run python manage.py createsuperuser
```

---

## Complete Setup Sequence

Here's the full sequence for setting up your database:

### On Your Local Machine:
```powershell
# 1. Activate virtual environment (if using one)
venv\Scripts\activate

# 2. Run migrations
python manage.py migrate

# 3. Create admin user
python manage.py createsuperuser

# 4. Start server
python manage.py runserver
```

### On Production Server (Railway/Render):

**Option A: Using Web Dashboard**
1. Open Shell/Terminal from your service dashboard
2. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

**Option B: Using Railway CLI**
```bash
railway login
railway link  # Link to your project
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

---

## Important Notes

### Migrations vs. Admin User:

| Task | Command | When to Run |
|------|---------|-------------|
| **Run Migrations** | `python manage.py migrate` | Every time you change models OR to sync Django with existing tables |
| **Create Admin User** | `python manage.py createsuperuser` | Once, to create your first admin account |

### If Tables Already Exist:

If you created tables manually (using SQL scripts):
- ✅ **Still run migrations** - Django will detect existing tables
- ✅ Django will mark migrations as "applied" without recreating tables
- ✅ This ensures Django knows about your tables

### After Running Migrations:

Test that everything works:
```python
python manage.py shell
>>> from inventory.models import Product
>>> Product.objects.count()  # Should work without error
```

---

## Troubleshooting

### "No changes detected"
This is **normal** if tables already exist. Django will still mark migrations as applied.

### "Table already exists"
This is also **normal**. Django will skip creating tables that already exist.

### "auth_user table does not exist"
First create auth tables:
```bash
python manage.py migrate auth
python manage.py migrate
```

### Can't create superuser because no users table?
Make sure you ran migrations first:
```bash
python manage.py migrate auth  # Creates user tables
python manage.py migrate        # Creates inventory tables
python manage.py createsuperuser  # Now this will work
```

---

## Quick Reference

```bash
# Run migrations (syncs database with models)
python manage.py migrate

# Create admin user (one-time setup)
python manage.py createsuperuser

# Check migration status
python manage.py showmigrations

# Create new migrations (after changing models)
python manage.py makemigrations
python manage.py migrate
```

