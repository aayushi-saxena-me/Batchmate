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
    
    # Get credentials from environment variables
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
    
    # Validate required fields
    if not username:
        print("❌ ERROR: DJANGO_SUPERUSER_USERNAME environment variable not set")
        print("\nSet it in Railway:")
        print("  Variables → New Variable")
        print("  Name: DJANGO_SUPERUSER_USERNAME")
        print("  Value: your_username")
        sys.exit(1)
    
    if not password:
        print("❌ ERROR: DJANGO_SUPERUSER_PASSWORD environment variable not set")
        print("\nSet it in Railway:")
        print("  Variables → New Variable")
        print("  Name: DJANGO_SUPERUSER_PASSWORD")
        print("  Value: your_secure_password")
        sys.exit(1)
    
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

