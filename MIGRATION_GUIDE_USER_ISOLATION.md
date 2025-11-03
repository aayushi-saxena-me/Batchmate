# Migration Guide: User Data Isolation

## Changes Made

### Models Updated:
1. **Category** - Added `created_by` field (required)
2. **Supplier** - Added `created_by` field (required)
3. **Product** - Made `created_by` required (removed `null=True`)
4. **Transaction** - Made `created_by` required (removed `null=True`)

### Constraints Added:
- Category names unique per user (`unique_together = ['name', 'created_by']`)
- Supplier names unique per user (`unique_together = ['name', 'created_by']`)
- Product SKU unique per user (`unique_together = ['sku', 'created_by']`)

### Views Updated:
- All views now filter by `request.user`
- Users can only see/edit their own data

### Forms Updated:
- Forms limit choices to user's data
- ProductForm limits category/supplier to user's
- TransactionForm limits products to user's

---

## Migration Steps

### Step 1: Create Migrations

```bash
python manage.py makemigrations inventory
```

This will create a migration file with:
- Adding `created_by` to Category
- Adding `created_by` to Supplier
- Making Product `created_by` required
- Making Transaction `created_by` required
- Updating unique constraints

### Step 2: Handle Existing Data

⚠️ **IMPORTANT**: If you have existing data, you need to handle it first!

**Option A: Assign to a Default User (if you have a superuser)**

Before running migrations, you can manually update existing records:

```python
# In Django shell: python manage.py shell
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction

# Get first user (or specific user)
default_user = User.objects.first()

# Assign existing data to this user
Category.objects.filter(created_by__isnull=True).update(created_by=default_user)
Supplier.objects.filter(created_by__isnull=True).update(created_by=default_user)
Product.objects.filter(created_by__isnull=True).update(created_by=default_user)
Transaction.objects.filter(created_by__isnull=True).update(created_by=default_user)
```

**Option B: Delete Existing Data (fresh start)**

If you don't need existing data:

```python
# In Django shell
from inventory.models import Category, Supplier, Product, Transaction

Transaction.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()
Supplier.objects.all().delete()
```

### Step 3: Run Migrations

```bash
python manage.py migrate inventory
```

Or if using `--fake-initial` (if tables already exist from SQL scripts):

```bash
python manage.py migrate inventory --fake-initial
```

---

## What Happens to Existing Data?

### If You Have Existing Data Without `created_by`:

**Category & Supplier:**
- Migration will fail if existing records don't have `created_by`
- Must assign to a user first (see Step 2)

**Product & Transaction:**
- If they have `null=True` currently, migration will work
- But new code requires them, so assign existing records

---

## Testing After Migration

1. **Create test users:**
   ```bash
   python manage.py createsuperuser  # User 1
   python manage.py createsuperuser  # User 2
   ```

2. **Test isolation:**
   - Login as User 1
   - Create products/categories/suppliers
   - Login as User 2
   - Should NOT see User 1's data
   - Create own data
   - Should only see own data

3. **Verify forms:**
   - Product form should only show User 1's categories/suppliers
   - Transaction form should only show User 1's products

---

## Rollback Plan

If migration fails:

1. **Check migration status:**
   ```bash
   python manage.py showmigrations inventory
   ```

2. **Unapply migration:**
   ```bash
   python manage.py migrate inventory <previous_migration_number>
   ```

3. **Fix data issues** (assign users to existing records)

4. **Re-run migration**

---

## SQL Scripts Update Needed

Your SQL scripts (`create_tables_postgresql.sql`, etc.) should be updated to include:
- `created_by_id` column in Category
- `created_by_id` column in Supplier
- Make `created_by_id` NOT NULL in Product and Transaction

But since you're using Django migrations now, the SQL scripts are mainly for reference.

---

## Summary

✅ Models updated with user ownership
✅ Views filter by user
✅ Forms limit to user data
⏳ **Next: Create and run migrations**

After migrations:
- Each user will have isolated inventory data
- Users cannot see/edit each other's data
- Data privacy maintained

