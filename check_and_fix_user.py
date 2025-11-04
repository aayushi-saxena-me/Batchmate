#!/usr/bin/env python
"""Check and fix user permissions"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth.models import User

# Find user by email or username
email_or_username = 'aayushi.saxena.me@gmail.com'
user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()

if user:
    print(f"\nUser found: {user.username}")
    print(f"Email: {user.email}")
    print(f"Is staff: {user.is_staff}")
    print(f"Is superuser: {user.is_superuser}")
    print(f"Is active: {user.is_active}")
    
    if not user.is_superuser or not user.is_staff:
        print("\n⚠️  User is NOT a superuser/staff. Making them a superuser...")
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print("✅ User is now a superuser!")
        print("\nYou can now access:")
        print("  - Django Admin: http://127.0.0.1:8000/admin/")
        print("  - User Report: http://127.0.0.1:8000/admin/user-report/")
        print("  - Create Admin: http://127.0.0.1:8000/accounts/create-superuser/")
    else:
        print("\n✅ User is already a superuser!")
else:
    print(f"\n❌ User with email '{email}' not found.")
    print("\nAvailable users:")
    for u in User.objects.all():
        print(f"  - {u.username} ({u.email}) - Superuser: {u.is_superuser}")

