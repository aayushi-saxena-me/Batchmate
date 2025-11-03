# Quick Testing Steps

## Fastest Way to Test

### Option 1: Automated Test (Recommended)

```bash
python test_user_isolation.py
```

This runs all tests automatically and reports results.

---

### Option 2: Manual Testing

#### Step 1: Run Migration

```bash
# Make sure you have a user
python manage.py createsuperuser

# Run migration
python manage.py migrate inventory
```

#### Step 2: Create Test Data

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product
from decimal import Decimal

# Create users if needed
user1, _ = User.objects.get_or_create(username='test1')
user2, _ = User.objects.get_or_create(username='test2')

# Create data for user1
Category.objects.create(name='User1 Category', created_by=user1)
Product.objects.create(name='User1 Product', sku='U1P001', quantity=10, created_by=user1)

# Create data for user2
Category.objects.create(name='User2 Category', created_by=user2)
Product.objects.create(name='User2 Product', sku='U2P001', quantity=20, created_by=user2)
```

#### Step 3: Test in Browser

```bash
python manage.py runserver
```

1. **Login as test1:**
   - Go to http://127.0.0.1:8000/products/
   - Should see ONLY "User1 Product"
   - Should NOT see "User2 Product"

2. **Logout and login as test2:**
   - Go to http://127.0.0.1:8000/products/
   - Should see ONLY "User2 Product"
   - Should NOT see "User1 Product"

**If both tests pass → ✅ User isolation works!**

---

## What to Check

✅ **Migration runs without errors**
✅ **All existing data has created_by**
✅ **Users can only see their own data**
✅ **Forms show only user's choices**
✅ **Unique constraints work per user**

---

## Full Testing Guide

See `TESTING_GUIDE.md` for comprehensive testing instructions.

