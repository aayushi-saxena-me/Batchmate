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
    if all_vars:
        print("   Found Django/Superuser variables:")
        for key, value in all_vars.items():
            # Mask password for security
            if 'PASSWORD' in key:
                print(f"     {key} = {'*' * len(value) if value else '(empty)'}")
            else:
                print(f"     {key} = '{value}'")
    else:
        print("   No DJANGO_SUPERUSER_* variables found")
    
    # Get credentials from environment variables
    # Use the dict we built since os.environ.get() might have issues
    username_raw = all_vars.get('DJANGO_SUPERUSER_USERNAME', '') if all_vars else os.environ.get('DJANGO_SUPERUSER_USERNAME', '')
    if not username_raw:
        # Fallback: search for the key (case-insensitive)
        for key, value in os.environ.items():
            if key.upper() == 'DJANGO_SUPERUSER_USERNAME':
                username_raw = value
                print(f"   🔍 Found username via search: '{key}' = '{value}'")
                break
    
    username = username_raw.strip() if username_raw else ''
    
    email_raw = all_vars.get('DJANGO_SUPERUSER_EMAIL', '') if all_vars else os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
    if not email_raw:
        for key, value in os.environ.items():
            if key.upper() == 'DJANGO_SUPERUSER_EMAIL':
                email_raw = value
                break
    
    email = email_raw.strip() if email_raw else ''
    
    password_raw = all_vars.get('DJANGO_SUPERUSER_PASSWORD', '') if all_vars else os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')
    if not password_raw:
        for key, value in os.environ.items():
            if key.upper() == 'DJANGO_SUPERUSER_PASSWORD':
                password_raw = value
                break
    
    password = password_raw.strip() if password_raw else ''
    
    # Debug: Show what we found
    print(f"\n📋 Values read:")
    print(f"   Username: '{username}' (length: {len(username)})")
    print(f"   Email: '{email}' (length: {len(email)})")
    print(f"   Password: {'*' * len(password) if password else '(empty)'} (length: {len(password)})")
    
    # Alternative: Try reading directly from environment dict
    try:
        username_alt = os.environ['DJANGO_SUPERUSER_USERNAME'].strip()
        print(f"   Username (direct access): '{username_alt}' (length: {len(username_alt)})")
        if username_alt and not username:
            print("   ⚠️  Direct access worked but .get() didn't - using direct value")
            username = username_alt
    except KeyError:
        print("   ⚠️  Direct access also failed - variable not found")
    except Exception as e:
        print(f"   ⚠️  Error with direct access: {e}")
    
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
    
    # Check if user already exists
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
    
    # Create new superuser
    try:
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
    except Exception as e:
        print(f"❌ Error creating superuser: {e}")
        sys.exit(1)

if __name__ == '__main__':
    create_superuser()

