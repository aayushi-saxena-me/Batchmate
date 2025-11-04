# How to Create a Superuser Locally

## Step-by-Step Instructions

### Step 1: Run the Command

Open your terminal/PowerShell in the project directory and run:

```bash
python manage.py createsuperuser
```

### Step 2: Enter the Information

You'll be prompted for the following (press Enter after each):

1. **Username:**
   ```
   Username (leave blank to use 'gtg09'): 
   ```
   - Enter a username (e.g., `admin` or `superuser`)
   - Or press Enter to use the default shown in parentheses

2. **Email address:**
   ```
   Email address: 
   ```
   - Enter an email (e.g., `admin@example.com`)
   - Or press Enter to leave blank (optional)

3. **Password:**
   ```
   Password: 
   ```
   - Enter a password (it won't show on screen - this is normal!)
   - Press Enter

4. **Password (again):**
   ```
   Password (again): 
   ```
   - Enter the same password again to confirm
   - Press Enter

### Step 3: Success Message

You should see:
```
Superuser created successfully.
```

## Example Session

Here's what a complete session looks like:

```bash
PS C:\Z Documents\Kids\Aayushi\Batchmate> python manage.py createsuperuser
Username (leave blank to use 'gtg09'): admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

## Important Notes

### Password Security
- The password won't show as you type (this is normal for security)
- Make sure to use a strong password
- Don't share your superuser password

### Username Validation
- Username must be unique
- If you get "That username is already taken", try a different username

### Email is Optional
- You can leave email blank by pressing Enter
- But it's recommended to provide one

## Troubleshooting

### "Command not found" or "No module named 'django'"

**Solution:** Activate your virtual environment first:

```powershell
# If you have venv folder
.\venv\Scripts\Activate.ps1

# Then run createsuperuser
python manage.py createsuperuser
```

### "django.db.utils.OperationalError: no such table: auth_user"

**Solution:** Run migrations first:

```bash
python manage.py migrate
python manage.py createsuperuser
```

### "That username is already taken"

**Solution:** 
- Use a different username, OR
- Check existing users:
  ```bash
  python manage.py shell
  ```
  ```python
  from django.contrib.auth.models import User
  print([u.username for u in User.objects.all()])
  ```

### Password Too Simple

**Solution:** Django might reject very simple passwords. Use:
- At least 8 characters
- Mix of letters, numbers, and symbols
- Not common words

## After Creating Superuser

### Test It

1. **Start your server:**
   ```bash
   python manage.py runserver
   ```

2. **Login:**
   - Go to: `http://127.0.0.1:8000/accounts/login/`
   - Use your superuser username and password

3. **Verify:**
   - You should see "User Report" and "Create Admin" links in the sidebar
   - These only appear for superusers

### Access Django Admin

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials
3. You'll have full admin access

## Quick Reference

```bash
# Create superuser
python manage.py createsuperuser

# Check existing users
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.filter(is_superuser=True)

# Start server
python manage.py runserver
```

## Next Steps

After creating your superuser:
1. ✅ Login to the application
2. ✅ Access "Create Admin" link in sidebar (to create more admins)
3. ✅ Access Django admin at `/admin/`
4. ✅ View User Report at `/admin/user-report/`

