# Migration Summary: Handling Existing Data

## The Question

**"How are you factoring the case that we already have data sitting in database that is not tied to any user? do we need to run any migration?"**

## The Answer

✅ **Yes, you need to run a migration.** I've created `0002_add_user_isolation.py` that handles existing data automatically.

---

## What I Created

### 1. **Migration File** (`inventory/migrations/0002_add_user_isolation.py`)

This migration:
- ✅ Adds `created_by` to Category and Supplier (if missing)
- ✅ Updates Product/Transaction `created_by` (changes to CASCADE)
- ✅ **Automatically assigns existing data to first user**
- ✅ Makes all `created_by` fields required
- ✅ Updates unique constraints to be per-user

### 2. **Documentation**
- `HANDLE_EXISTING_DATA_MIGRATION.md` - Detailed guide
- `MIGRATION_STEPS_COMPLETE.md` - Quick reference
- `assign_existing_data_to_user.sql` - Manual SQL alternative

---

## How It Handles Existing Data

### The Migration Process:

```
Step 1: Add created_by fields (nullable)
        ↓
Step 2: Assign existing records to first user
        (automatically - all records get user)
        ↓
Step 3: Make fields required (NOT NULL)
        ↓
Step 4: Update constraints (per-user uniqueness)
```

### The Key Function:

```python
def assign_existing_data_to_default_user(apps, schema_editor):
    # Gets first user from database
    # Assigns all records without created_by to that user
```

**This runs automatically when you execute the migration!**

---

## Your Situation

Since you created tables manually via SQL:

### Scenario A: Tables Created via SQL, Some Have created_by_id

If your SQL created:
- ✅ Product and Transaction with `created_by_id` (nullable)
- ❌ Category and Supplier without `created_by_id`

**The migration will:**
1. Add `created_by_id` to Category/Supplier
2. Find all records where `created_by_id IS NULL`
3. Assign them to first user
4. Make all required

### Scenario B: Tables Created via SQL, None Have created_by_id

**The migration will:**
1. Add `created_by_id` to all tables
2. Assign all existing records to first user
3. Make all required

---

## Required Steps

### Before Migration:

```bash
# 1. Ensure at least one user exists
python manage.py createsuperuser
```

### Run Migration:

```bash
# 2. Run the migration (handles everything automatically)
python manage.py migrate inventory
```

**That's it!** The migration assigns existing data automatically.

---

## What Happens to Your Data

### All Existing Records:
- Category records → Assigned to first user
- Supplier records → Assigned to first user  
- Product records → Assigned to first user (if NULL)
- Transaction records → Assigned to first user (if NULL)

### After Migration:
- ✅ All records have `created_by`
- ✅ All records belong to a user
- ✅ Users can only see their own data
- ✅ No data loss

---

## Verification

After migration, verify it worked:

```bash
python manage.py shell
```

```python
from inventory.models import *
from django.contrib.auth.models import User

# Check all records have a user
print(f"Categories without user: {Category.objects.filter(created_by__isnull=True).count()}")
print(f"Suppliers without user: {Supplier.objects.filter(created_by__isnull=True).count()}")
print(f"Products without user: {Product.objects.filter(created_by__isnull=True).count()}")
print(f"Transactions without user: {Transaction.objects.filter(created_by__isnull=True).count()}")

# All should be 0!

# Check how many records were assigned
user = User.objects.first()
print(f"\n{user.username} owns:")
print(f"  {Category.objects.filter(created_by=user).count()} categories")
print(f"  {Supplier.objects.filter(created_by=user).count()} suppliers")
print(f"  {Product.objects.filter(created_by=user).count()} products")
print(f"  {Transaction.objects.filter(created_by=user).count()} transactions")
```

---

## If Migration Fails

### Error: "No users found"

**Fix:**
```bash
python manage.py migrate auth  # Creates user tables
python manage.py createsuperuser  # Create user
python manage.py migrate inventory  # Now works
```

### Error: "Column already exists"

If tables were created via SQL and columns exist:
- Migration might detect and skip
- If it fails, use `--fake` flag: `python manage.py migrate inventory 0002 --fake`

---

## Alternative: Manual Assignment

If you prefer to assign data manually before migration:

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction

user = User.objects.first()  # or get specific user

# Manually assign
Category.objects.filter(created_by__isnull=True).update(created_by=user)
Supplier.objects.filter(created_by__isnull=True).update(created_by=user)
Product.objects.filter(created_by__isnull=True).update(created_by=user)
Transaction.objects.filter(created_by__isnull=True).update(created_by=user)
```

Then run migration - assignment step will see all records have users and skip.

---

## Summary

✅ **Migration created** - Handles everything automatically
✅ **Existing data handled** - All records assigned to first user
✅ **No data loss** - All records preserved
✅ **Safe** - Runs in transaction, can rollback
✅ **One command** - `python manage.py migrate inventory`

**Just make sure you have a user first!**

