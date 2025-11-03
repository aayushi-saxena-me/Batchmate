# Complete Migration Steps for User Isolation

## Overview

Since you have existing data in the database, we need to handle it before making `created_by` required.

---

## Two Approaches

### Approach A: Use Django Migration (Recommended)

**Pros:** 
- Automatic
- Handles all edge cases
- Can rollback easily
- Django tracks it

**Cons:**
- Requires user to exist first

**Steps:**
1. Ensure at least one user exists: `python manage.py createsuperuser`
2. Run: `python manage.py migrate inventory`
3. Migration automatically assigns existing data to first user

---

### Approach B: Manual SQL Script

**Pros:**
- More control
- Can see exactly what's happening
- Works if Django migrations are problematic

**Cons:**
- Manual steps
- Need to verify results

**Steps:**
1. Run `assign_existing_data_to_user.sql`
2. Then run: `python manage.py migrate inventory --fake`

---

## Recommended: Approach A

### Step-by-Step

#### 1. Check Existing Data

```bash
python manage.py shell
```

```python
from inventory.models import Category, Supplier, Product, Transaction
print(f"Categories: {Category.objects.count()}")
print(f"Suppliers: {Supplier.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Transactions: {Transaction.objects.count()}")
```

#### 2. Ensure User Exists

```bash
# Check if users exist
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.count()

# If 0, create one:
python manage.py createsuperuser
```

#### 3. Run Migration

```bash
python manage.py migrate inventory
```

The migration (`0002_add_user_isolation.py`) will:
- ✅ Add `created_by` fields
- ✅ Assign all existing data to first user
- ✅ Make fields required
- ✅ Update constraints

---

## What the Migration Does

The migration file I created handles everything:

```python
# 1. Adds created_by fields (nullable)
# 2. Assigns existing records to first user
assign_existing_data_to_default_user()
# 3. Makes fields required
# 4. Updates unique constraints
```

---

## Verification After Migration

```bash
python manage.py shell
```

```python
from inventory.models import *
from django.contrib.auth.models import User

user = User.objects.first()
print(f"Categories for {user.username}: {Category.objects.filter(created_by=user).count()}")
print(f"Suppliers for {user.username}: {Supplier.objects.filter(created_by=user).count()}")
print(f"Products for {user.username}: {Product.objects.filter(created_by=user).count()}")
print(f"Transactions for {user.username}: {Transaction.objects.filter(created_by=user).count()}")

# Should match total counts!
```

---

## If You Have Multiple Users

If you want to distribute existing data across users, do it manually BEFORE migration:

```python
# In Django shell
from django.contrib.auth.models import User
from inventory.models import *

user1 = User.objects.get(username='user1')
user2 = User.objects.get(username='user2')

# Example: Assign first half to user1, second half to user2
products = Product.objects.filter(created_by__isnull=True)
for i, product in enumerate(products):
    product.created_by = user1 if i < len(products) // 2 else user2
    product.save()
```

Then run migration (assignment step will be skipped since all have users).

---

## Troubleshooting

### "No users found" Error

**Fix:**
```bash
python manage.py migrate auth  # Creates user tables
python manage.py createsuperuser  # Create user
python manage.py migrate inventory  # Now this will work
```

### Migration Fails on Data Assignment

**Manual fix:**
```python
python manage.py shell
>>> from django.contrib.auth.models import User
>>> from inventory.models import *
>>> user = User.objects.first()
>>> Category.objects.filter(created_by__isnull=True).update(created_by=user)
>>> Supplier.objects.filter(created_by__isnull=True).update(created_by=user)
>>> Product.objects.filter(created_by__isnull=True).update(created_by=user)
>>> Transaction.objects.filter(created_by__isnull=True).update(created_by=user)
```

Then continue migration.

---

## Summary

✅ **Migration file created** - `inventory/migrations/0002_add_user_isolation.py`
✅ **Handles existing data** - Automatically assigns to first user
✅ **Safe** - Runs in transaction, can rollback
✅ **Complete** - All steps automated

**Just ensure you have a user first, then run:**
```bash
python manage.py migrate inventory
```

