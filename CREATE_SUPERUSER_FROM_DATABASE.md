# Create Superuser Directly from Database/Environment Variables

## Method 1: Using Environment Variables (Recommended)

This is the easiest way for deployment - no interactive prompts needed!

### Step 1: Set Environment Variables in Railway

Go to Railway Dashboard → Your Web Service → Variables tab:

Add these variables:
```
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password_here
```

⚠️ **Important:** Use a strong password! Don't use "admin123" or "password"

### Step 2: Run the Script

In Railway shell/command:
```bash
python create_superuser_from_env.py
```

**That's it!** The script will:
- ✅ Read credentials from environment variables
- ✅ Create the superuser automatically
- ✅ Skip if superuser already exists
- ✅ No prompts needed!

### Step 3: Update Procfile (Optional - Auto-Run)

You can add this to your `Procfile` to auto-create superuser on deployment:

```bash
release: python manage.py migrate --noinput && python create_superuser_from_env.py
web: gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Note:** This will only create if environment variables are set and user doesn't exist.

---

## Method 2: Direct SQL (Advanced)

If you really want to use SQL directly, here's how:

### PostgreSQL

```sql
-- First, you need to hash the password using Django's password hasher
-- Django uses PBKDF2SHA256 by default
-- The hash format is: algorithm$iterations$salt$hash

-- Example for password "admin123" (you need to generate this properly)
-- Use Python to generate the hash first:

-- In Python shell:
-- from django.contrib.auth.hashers import make_password
-- print(make_password('your_password'))

-- Then insert:
INSERT INTO auth_user (
    username,
    password,
    email,
    is_superuser,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'admin',
    'pbkdf2_sha256$600000$...generated_hash...',  -- Use make_password() output
    'admin@example.com',
    true,
    true,
    true,
    NOW()
);
```

### SQLite

```sql
INSERT INTO auth_user (
    username,
    password,
    email,
    is_superuser,
    is_staff,
    is_active,
    date_joined
) VALUES (
    'admin',
    'pbkdf2_sha256$600000$...generated_hash...',  -- Use make_password() output
    'admin@example.com',
    1,
    1,
    1,
    datetime('now')
);
```

### Generate Password Hash (Required for SQL Method)

You MUST generate the password hash first. Run this in Python:

```python
from django.contrib.auth.hashers import make_password
password = 'your_password_here'
hashed = make_password(password)
print(hashed)
```

Copy the output and use it in the SQL INSERT statement above.

---

## Method 3: Python Script (Simpler SQL Alternative)

Create a script that uses Django's ORM (no password hashing needed):

```python
# create_admin.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'your_secure_password'

if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists")
else:
    User.objects.create_superuser(username, email, password)
    print(f"Superuser '{username}' created!")
```

Run: `python create_admin.py`

---

## Recommended: Use Method 1 (Environment Variables)

**Why:**
- ✅ No interactive prompts
- ✅ Works in deployment
- ✅ Secure (password in environment variable, not in code)
- ✅ Easy to update
- ✅ Can be automated

**Setup:**
1. Set environment variables in Railway
2. Run `python create_superuser_from_env.py`
3. Done!

---

## Quick Setup for Railway

### Option A: One-Time Setup (Manual)

1. **Set variables in Railway:**
   - `DJANGO_SUPERUSER_USERNAME=admin`
   - `DJANGO_SUPERUSER_EMAIL=admin@example.com`
   - `DJANGO_SUPERUSER_PASSWORD=your_secure_password`

2. **Run script:**
   ```bash
   railway run python create_superuser_from_env.py
   ```

### Option B: Auto-Run on Deploy

Update `Procfile`:
```bash
release: python manage.py migrate --noinput && python create_superuser_from_env.py || true
web: gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

The `|| true` means it won't fail if superuser already exists.

---

## Security Notes

⚠️ **Important:**
- Use strong passwords (at least 12 characters, mix of letters/numbers/symbols)
- Don't commit passwords to git
- Use environment variables (not hardcoded)
- Rotate passwords regularly
- Railway encrypts environment variables at rest

---

## Troubleshooting

### "Environment variable not set"
- Make sure you set `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` in Railway Variables
- Check spelling (case-sensitive)

### "User already exists"
- The script will skip creation if user exists
- Or update existing user to superuser

### "Password too simple"
- Django validates passwords
- Use at least 8 characters
- Mix of letters, numbers, symbols

---

## Summary

**Best Method:** Use `create_superuser_from_env.py` with environment variables

**Steps:**
1. Set `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` in Railway
2. Run: `python create_superuser_from_env.py`
3. Login with those credentials

**No interactive prompts needed!** 🎉

