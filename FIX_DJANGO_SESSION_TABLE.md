# Fix: "relation django_session does not exist" Error

## The Problem

When trying to log in, you get this error:
```
django.db.utils.ProgrammingError: relation "django_session" does not exist
```

## Root Cause

The `django_session` table is missing. Django uses this table to store session data when users log in. Since you created tables manually, you likely didn't create the Django system tables (sessions, contenttypes, etc.).

## The Solution

Run Django migrations to create all missing Django system tables:

```bash
python manage.py migrate
```

This will create:
- ✅ `django_session` - Stores user sessions (needed for login)
- ✅ `django_content_type` - Content types system
- ✅ `django_migrations` - Migration tracking
- ✅ Other Django system tables

---

## Step-by-Step Fix

### Option 1: Run All Migrations (Recommended)

This ensures ALL Django system tables are created:

```bash
python manage.py migrate
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying sessions.0001_initial... OK    # This creates django_session!
  Applying admin.0001_initial... OK
  Applying inventory.0001_initial... OK
```

### Option 2: Run Only Sessions Migration

If you just want the session table:

```bash
python manage.py migrate sessions
```

---

## Why This Happens

When you created tables manually using SQL scripts, you only created:
- `inventory_category`
- `inventory_supplier`
- `inventory_product`
- `inventory_transaction`

But Django needs additional system tables:
- `django_session` - For login sessions
- `django_content_type` - For content types
- `auth_user` - For users (you probably have this)
- `auth_group`, `auth_permission` - For permissions
- `django_migrations` - To track migrations

---

## Verify the Fix

After running migrations:

1. **Check if django_session exists:**
   ```bash
   python manage.py dbshell
   ```
   Then:
   ```sql
   \dt  -- List all tables (should see django_session)
   ```

2. **Try logging in again** - should work now!

---

## Quick Fix Command

In Railway Shell or locally:

```bash
python manage.py migrate
```

That's it! This will create all missing Django system tables including `django_session`.

---

## What Each Django App Creates

| Django App | Tables Created | Purpose |
|------------|----------------|---------|
| `sessions` | `django_session` | Store user session data (login) |
| `contenttypes` | `django_content_type`, etc. | Content type system |
| `auth` | `auth_user`, `auth_group`, etc. | User authentication |
| `admin` | Uses contenttypes | Admin interface |
| `inventory` | `inventory_*` tables | Your app tables |

---

## After Fixing

✅ You'll be able to:
- Log in successfully
- Maintain sessions across requests
- Use Django's session framework

The login will work because Django can now store session data in the `django_session` table!

