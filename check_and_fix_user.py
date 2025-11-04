#!/usr/bin/env python
"""Check and fix user permissions"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')

try:
    django.setup()
except Exception as e:
    print(f"\n❌ Error setting up Django: {e}")
    sys.exit(1)

try:
    from django.contrib.auth.models import User
    from django.db import connection
    
    # Check if auth_user table exists (works for both SQLite and PostgreSQL)
    with connection.cursor() as cursor:
        db_engine = connection.vendor
        if db_engine == 'sqlite':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='auth_user';")
        else:  # PostgreSQL, MySQL, etc.
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' AND tablename='auth_user';")
        table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        print("\n❌ ERROR: auth_user table does not exist!")
        print("\nYou need to run migrations first:")
        print("  python manage.py migrate")
        print("\nOr in deployment:")
        print("  railway run python manage.py migrate")
        print("  # or")
        print("  # In Railway dashboard: Deployments → Run Command → python manage.py migrate")
        sys.exit(1)
except Exception as e:
    print(f"\n❌ Database error: {e}")
    print("\nThis usually means migrations haven't been run.")
    print("Run: python manage.py migrate")
    sys.exit(1)

# Find user by email or username
email_or_username = 'aayushi.saxena.me@gmail.com'
try:
    user = User.objects.filter(email=email_or_username).first() or User.objects.filter(username=email_or_username).first()
except Exception as e:
    print(f"\n❌ Error querying users: {e}")
    print("\nThis usually means migrations haven't been run.")
    print("Run: python manage.py migrate")
    sys.exit(1)

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

