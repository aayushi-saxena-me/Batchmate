# Handling Existing Data During User Isolation Migration

## The Problem

You have existing inventory data in your database that was created before user isolation. This data doesn't have `created_by` fields set, but the new models require them.

## The Solution

I've created a **custom migration** (`0002_add_user_isolation.py`) that:
1. ✅ Adds `created_by` fields as nullable first
2. ✅ Assigns existing records to a default user automatically
3. ✅ Makes fields required after assignment
4. ✅ Updates unique constraints

---

## Migration Strategy

The migration does this in steps:

### Step 1-2: Add Fields (Nullable)
- Adds `created_by` to Category and Supplier (nullable)
- Updates Product/Transaction `created_by` (still nullable)

### Step 3-4: Update Foreign Keys
- Changes from `SET_NULL` to `CASCADE` (but keeps nullable)

### Step 5: **Assign Existing Data**
- Automatically assigns all existing records to the **first user** in your database
- This is usually your superuser/admin account

### Step 6-7: Remove Old Unique Constraints
- Removes global unique constraint from Category.name
- Removes global unique constraint from Product.sku

### Step 8: Make Fields Required
- Sets `created_by` to NOT NULL (now safe since all records have it)

### Step 9-10: Add Per-User Constraints & Indexes
- Adds unique constraints per user
- Adds performance indexes

---

## Before Running Migration

### Option A: Ensure You Have a User (Recommended)

If you have existing data, make sure at least one user exists:

```bash
# Create a superuser first
python manage.py createsuperuser
```

This user will "own" all existing data.

### Option B: Check if Users Exist

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
print(f"Users in database: {User.objects.count()}")
if User.objects.exists():
    print(f"First user: {User.objects.first().username}")
else:
    print("No users found - create one first!")
```

---

## Running the Migration

### Step 1: Create the Migration File

The migration file `0002_add_user_isolation.py` is already created in `inventory/migrations/`.

### Step 2: Run the Migration

```bash
python manage.py migrate inventory
```

The migration will:
1. Add the fields
2. Automatically assign existing data to first user
3. Make fields required
4. Update constraints

### Step 3: Verify

```bash
python manage.py shell
```

```python
from inventory.models import Category, Supplier, Product, Transaction
from django.contrib.auth.models import User

# Check all records have created_by
print(f"Categories without user: {Category.objects.filter(created_by__isnull=True).count()}")
print(f"Suppliers without user: {Supplier.objects.filter(created_by__isnull=True).count()}")
print(f"Products without user: {Product.objects.filter(created_by__isnull=True).count()}")
print(f"Transactions without user: {Transaction.objects.filter(created_by__isnull=True).count()}")

# Should all be 0!
```

---

## What If Migration Fails?

### Error: "No users found"

**Fix:**
```bash
# 1. First create auth tables
python manage.py migrate auth

# 2. Create a user
python manage.py createsuperuser

# 3. Run migration again
python manage.py migrate inventory
```

### Error: "Cannot add NOT NULL column"

This means the data assignment step failed.

**Fix:** Manually assign data first:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction

default_user = User.objects.first()  # or User.objects.get(username='admin')

Category.objects.filter(created_by__isnull=True).update(created_by=default_user)
Supplier.objects.filter(created_by__isnull=True).update(created_by=default_user)
Product.objects.filter(created_by__isnull=True).update(created_by=default_user)
Transaction.objects.filter(created_by__isnull=True).update(created_by=default_user)
```

Then continue with migration.

### Error: "Unique constraint violation"

If you have duplicate category/supplier names or product SKUs, the per-user unique constraint might fail.

**Fix:** Either:
1. Delete duplicates
2. Or modify the migration to handle duplicates

---

## Manual Assignment (Alternative)

If you prefer to manually assign data BEFORE migration:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction

# Option 1: Assign to first user
user = User.objects.first()
Category.objects.filter(created_by__isnull=True).update(created_by=user)
Supplier.objects.filter(created_by__isnull=True).update(created_by=user)
Product.objects.filter(created_by__isnull=True).update(created_by=user)
Transaction.objects.filter(created_by__isnull=True).update(created_by=user)

# Option 2: Assign to specific user
user = User.objects.get(username='admin')
# ... same update commands

# Option 3: Assign different records to different users
# (More complex - would need custom logic)
```

Then run:
```bash
python manage.py migrate inventory
```

The migration will see that all records have `created_by` and skip the assignment step.

---

## For Your Specific Situation

Since you created tables manually via SQL:

1. **Check if tables have `created_by_id` columns:**
   ```sql
   -- In PostgreSQL
   \d inventory_category
   \d inventory_supplier
   \d inventory_product
   \d inventory_transaction
   ```

2. **If columns don't exist:**
   - Migration will add them
   - Then assign existing data to a user

3. **If columns exist but are NULL:**
   - Migration will assign them to first user

4. **If you have data and want to keep it:**
   - Create a superuser first
   - Run migration - it will assign data to that user

---

## Important Notes

### Default User Assignment:
- All existing data will be assigned to the **first user** in your database
- This is usually your admin/superuser account
- If you have multiple users and want to distribute data, do it manually before migration

### Data Safety:
- The migration uses `RunPython` which runs in a transaction
- If it fails, nothing is changed (atomic)
- You can rollback if needed

### Production Considerations:
- **Backup your database first!**
- Test migration on a copy of production data
- Have a rollback plan

---

## Quick Start (Fresh Database)

If you don't have important data:

```bash
# Delete existing data
python manage.py shell
>>> from inventory.models import *
>>> Transaction.objects.all().delete()
>>> Product.objects.all().delete()
>>> Category.objects.all().delete()
>>> Supplier.objects.all().delete()

# Then run migration
python manage.py migrate inventory
```

---

## Summary

✅ Migration automatically handles existing data
✅ Assigns all existing records to first user
✅ Safe (runs in transaction)
✅ No data loss

**Just make sure you have at least one user before running the migration!**

