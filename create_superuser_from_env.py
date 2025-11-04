#!/usr/bin/env python
"""
Create superuser from environment variables
No interactive prompts needed - perfect for deployment!

Usage:
  Set these environment variables:
    DJANGO_SUPERUSER_USERNAME=admin
    DJANGO_SUPERUSER_EMAIL=admin@example.com
    DJANGO_SUPERUSER_PASSWORD=your_secure_password

  Then run:
    python create_superuser_from_env.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
try:
    django.setup()
except Exception as e:
    print(f"❌ Error setting up Django: {e}")
    sys.exit(1)

from django.contrib.auth.models import User

def create_superuser():
    """Create superuser from environment variables"""
    
    # Debug: Print all environment variables (for troubleshooting)
    print("🔍 Debug: Checking environment variables...")
    all_vars = {k: v for k, v in os.environ.items() if 'SUPERUSER' in k or 'DJANGO' in k}
    
    # Find the actual keys (handle any whitespace or case issues)
    username_key = None
    email_key = None
    password_key = None
    
    if all_vars:
        print("   Found Django/Superuser variables:")
        for key, value in all_vars.items():
            # Clean key - remove newlines and whitespace
            key_clean = key.strip().replace('\n', '').replace('\r', '')
            
            # Mask password for security
            if 'PASSWORD' in key_clean:
                print(f"     {key_clean} = {'*' * len(value) if value else '(empty)'}")
                if 'SUPERUSER' in key_clean and not password_key:
                    password_key = key  # Use original key for dict lookup
                    print(f"        → Using this key for password: '{key_clean}'")
            else:
                print(f"     {key_clean} = '{value}'")
                if 'USERNAME' in key_clean and 'SUPERUSER' in key_clean and not username_key:
                    username_key = key  # Use original key for dict lookup
                    print(f"        → Using this key for username: '{key_clean}'")
                elif 'EMAIL' in key_clean and 'SUPERUSER' in key_clean and not email_key:
                    email_key = key  # Use original key for dict lookup
                    print(f"        → Using this key for email: '{key_clean}'")
    else:
        print("   No DJANGO_SUPERUSER_* variables found")
    
    # Get credentials using the actual keys we found during iteration
    username_raw = ''
    email_raw = ''
    password_raw = ''
    
    # Get username - handle keys with newlines/whitespace
    if username_key and username_key in all_vars:
        username_raw = all_vars[username_key]
        print(f"\n   ✅ Username found using key '{username_key.strip().replace(chr(10), '').replace(chr(13), '')}': '{username_raw}'")
    else:
        # Fallback: try exact key (cleaned)
        exact_key = 'DJANGO_SUPERUSER_USERNAME'
        username_raw = all_vars.get(exact_key, '') if all_vars else ''
        if not username_raw:
            # Fallback: search for the key (case-insensitive, handle whitespace)
            for key, value in os.environ.items():
                key_clean = key.strip().upper().replace('\n', '').replace('\r', '')
                if 'USERNAME' in key_clean and 'SUPERUSER' in key_clean and 'DJANGO' in key_clean:
                    username_raw = value
                    username_key = key
                    print(f"   🔍 Found username via search: '{key}' = '{value}'")
                    break
    
    # Clean username - remove any newlines, whitespace, etc.
    username = username_raw.strip() if username_raw else ''
    username = username.replace('\n', '').replace('\r', '').strip()
    
    # Debug: Show cleaned value
    if username_raw:
        print(f"   Raw username: {repr(username_raw)}")
        print(f"   Cleaned username: {repr(username)}")
    
    if email_key and email_key in all_vars:
        email_raw = all_vars[email_key]
        print(f"   ✅ Email found using key '{email_key}': '{email_raw}'")
    else:
        email_raw = all_vars.get('DJANGO_SUPERUSER_EMAIL', '') if all_vars else ''
        if not email_raw:
            for key, value in os.environ.items():
                if 'EMAIL' in key and 'SUPERUSER' in key and 'DJANGO' in key:
                    email_raw = value
                    email_key = key
                    break
    
    email = email_raw.strip() if email_raw else ''
    
    if password_key and password_key in all_vars:
        password_raw = all_vars[password_key]
        print(f"   ✅ Password found using key '{password_key}'")
    else:
        password_raw = all_vars.get('DJANGO_SUPERUSER_PASSWORD', '') if all_vars else ''
        if not password_raw:
            for key, value in os.environ.items():
                if 'PASSWORD' in key and 'SUPERUSER' in key and 'DJANGO' in key:
                    password_raw = value
                    password_key = key
                    break
    
    password = password_raw.strip() if password_raw else ''
    
    # Debug: Show what we found
    print(f"\n📋 Final values:")
    print(f"   Username: '{username}' (length: {len(username)})")
    print(f"   Email: '{email}' (length: {len(email)})")
    print(f"   Password: {'*' * len(password) if password else '(empty)'} (length: {len(password)})")
    
    # Check for placeholder values
    placeholder_values = ['your_username', 'your_secure_password', 'admin@example.com', '']
    
    # Validate required fields
    if not username or username.lower() in [p.lower() for p in placeholder_values if p]:
        print("\n⚠️  WARNING: DJANGO_SUPERUSER_USERNAME not set or is placeholder")
        print(f"   Current value: '{username}'")
        print(f"   Is empty: {not username}")
        print(f"   Is placeholder: {username.lower() in [p.lower() for p in placeholder_values if p]}")
        print("\n   Skipping superuser creation (this is OK if you'll create it manually)")
        print("   To enable auto-creation, set in Railway Variables:")
        print("     Name: DJANGO_SUPERUSER_USERNAME")
        print("     Value: admin (or your desired username)")
        return  # Exit gracefully instead of failing
    
    if not password or password.lower() in [p.lower() for p in placeholder_values if p]:
        print("\n⚠️  WARNING: DJANGO_SUPERUSER_PASSWORD not set or is placeholder")
        print(f"   Password length: {len(password)}")
        print("\n   Skipping superuser creation (this is OK if you'll create it manually)")
        print("   To enable auto-creation, set in Railway Variables:")
        print("     Name: DJANGO_SUPERUSER_PASSWORD")
        print("     Value: your_secure_password_here")
        return  # Exit gracefully instead of failing
    
    # Check if user already exists (with error handling)
    try:
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.is_superuser:
                print(f"✅ Superuser '{username}' already exists!")
                print(f"   Email: {user.email or '(not set)'}")
                print(f"   Is superuser: {user.is_superuser}")
                print(f"   Is staff: {user.is_staff}")
                return
            else:
                print(f"⚠️  User '{username}' exists but is not a superuser.")
                print("   Making them a superuser...")
                user.is_superuser = True
                user.is_staff = True
                user.set_password(password)
                if email:
                    user.email = email
                user.save()
                print(f"✅ User '{username}' is now a superuser!")
                return
    except Exception as db_error:
        print(f"⚠️  Database error while checking existing user: {db_error}")
        print("   This might mean migrations haven't run yet or database isn't ready")
        print("   Will attempt to create user anyway...")
        # Continue to creation attempt
    
    # Create new superuser
    try:
        print(f"\n🔧 Attempting to create superuser...")
        print(f"   Username: '{username}' (length: {len(username)})")
        print(f"   Email: '{email}' (length: {len(email)})")
        print(f"   Password: {'*' * len(password)} (length: {len(password)})")
        
        # Validate before creating
        if not username:
            raise ValueError("Username is empty after cleaning")
        if not password:
            raise ValueError("Password is empty")
        
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Superuser '{username}' created successfully!")
        print(f"   Email: {email or '(not set)'}")
        print(f"   Username: {username}")
        print("\nYou can now login at:")
        print("  - Django Admin: /admin/")
        print("  - Main App: /accounts/login/")
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        print("   Skipping superuser creation")
        return  # Exit gracefully
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        # Don't exit - let deployment continue
        print("   Skipping superuser creation (deployment will continue)")
        return

if __name__ == '__main__':
    create_superuser()

