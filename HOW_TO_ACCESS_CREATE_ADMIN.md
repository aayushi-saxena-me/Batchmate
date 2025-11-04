# How to Access "Create Admin" Link in Sidebar

## Quick Answer

The "Create Admin" link appears in the sidebar **only if you're logged in as a superuser**.

## Steps to Access It

### Step 1: Make Sure You Have a Superuser Account

If you don't have a superuser yet, create one first:

**Option A: Using Command Line (Recommended for first time)**
```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password (twice)

**Option B: Using Django Admin** (if you already have a superuser)
1. Go to: `http://127.0.0.1:8000/admin/`
2. Login as superuser
3. Navigate to "Users" → Add user
4. Create new user and check "Superuser status"

### Step 2: Login as Superuser

1. Start your server (if not running):
   ```bash
   python manage.py runserver
   ```

2. Go to: `http://127.0.0.1:8000/accounts/login/`

3. Login with your superuser credentials

### Step 3: Look for "Create Admin" in Sidebar

Once logged in as superuser, you should see:
- **Dashboard**
- **Products**
- **Categories**
- **Suppliers**
- **User Report** ← (only for superusers)
- **Create Admin** ← (only for superusers) ← **THIS IS IT!**
- **Logout**

The "Create Admin" link appears between "User Report" and "Logout" in the sidebar.

## Visual Guide

```
┌─────────────────────┐
│   Inventory         │
├─────────────────────┤
│ Dashboard           │
│ Products            │
│ Categories          │
│ Suppliers           │
├─────────────────────┤
│ User Report         │ ← Only for superusers
│ Create Admin        │ ← Only for superusers (THIS ONE!)
├─────────────────────┤
│ Logout              │
└─────────────────────┘
```

## Alternative Ways to Access

### Option 1: Direct URL
If you're logged in as superuser, go directly to:
```
http://127.0.0.1:8000/accounts/create-superuser/
```

### Option 2: From User Report Page
1. Login as superuser
2. Click "User Report" in sidebar
3. Click the green "Create Admin User" button at the top

## Troubleshooting

### "Create Admin" Link Not Showing?

**Problem:** You're not logged in as a superuser.

**Solution:**
1. Check if you're logged in: Look for your username in the sidebar
2. Check if you're a superuser:
   ```bash
   python manage.py shell
   ```
   ```python
   from django.contrib.auth.models import User
   user = User.objects.get(username='your_username')
   print(f"Is superuser: {user.is_superuser}")
   ```
3. If `False`, you need to create a superuser account first:
   ```bash
   python manage.py createsuperuser
   ```

### "Forbidden (403)" When Accessing Directly?

**Problem:** You're not a superuser.

**Solution:** Create a superuser account first using command line.

### Can't See Any Sidebar?

**Problem:** You're not logged in.

**Solution:**
1. Go to: `http://127.0.0.1:8000/accounts/login/`
2. Login with your credentials
3. Sidebar will appear after login

## Quick Test

To verify you're a superuser:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User

# List all superusers
superusers = User.objects.filter(is_superuser=True)
for user in superusers:
    print(f"Superuser: {user.username}")
```

If the list is empty, create one:
```bash
python manage.py createsuperuser
```

## Summary

**To see "Create Admin" link:**
1. ✅ Have a superuser account (create with `createsuperuser` if needed)
2. ✅ Login as that superuser
3. ✅ Look in the sidebar - it's between "User Report" and "Logout"

**Direct URL** (if logged in as superuser):
```
http://127.0.0.1:8000/accounts/create-superuser/
```

## First Time Setup

If this is your first time setting up:

1. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

2. **Start server:**
   ```bash
   python manage.py runserver
   ```

3. **Login:**
   - Go to: `http://127.0.0.1:8000/accounts/login/`
   - Login with your superuser credentials

4. **Access Create Admin:**
   - Look in sidebar for "Create Admin" link
   - Or go directly to: `http://127.0.0.1:8000/accounts/create-superuser/`

Now you can create additional admin users from the web interface!

