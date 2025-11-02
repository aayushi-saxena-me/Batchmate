# What Does `python manage.py migrate` Do?

## Simple Answer

`python manage.py migrate` **applies database schema changes** to make your database match your Django models. It's Django's way of keeping your database structure in sync with your code.

---

## Detailed Explanation

### The Two-Step Process

Django migrations work in **two steps**:

#### Step 1: `python manage.py makemigrations` (Create Migration Files)
- **When:** After you change your models (add/remove fields, create new models, etc.)
- **What it does:** Creates Python files in `inventory/migrations/` that describe the database changes
- **Example:** You add a new field to the Product model → `makemigrations` creates a file saying "add this field"

#### Step 2: `python manage.py migrate` (Apply Changes to Database)
- **When:** To actually update your database
- **What it does:** Reads those migration files and executes the SQL commands to change your database
- **Example:** Takes the migration file and runs `ALTER TABLE inventory_product ADD COLUMN new_field...`

---

## What `migrate` Actually Does

When you run `python manage.py migrate`, Django:

### 1. **Checks Which Migrations Have Been Applied**
- Looks at the `django_migrations` table in your database
- Compares with migration files in your `migrations/` folder
- Identifies which migrations haven't been run yet

### 2. **Applies Pending Migrations**
- Runs each unapplied migration in order
- Executes SQL commands to:
  - Create tables
  - Add/remove columns
  - Add/remove indexes
  - Add/remove foreign keys
  - Modify constraints

### 3. **Updates Migration Tracking**
- Records each applied migration in `django_migrations` table
- This prevents migrations from running twice

---

## What You'll See

### When Tables Don't Exist (Fresh Database):
```bash
$ python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, inventory, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying inventory.0001_initial... OK      # Creates inventory_product, etc.
  Applying sessions.0001_initial... OK
```

### When Tables Already Exist (Your Situation):
```bash
$ python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, inventory, sessions
Running migrations:
  No migrations to apply.                    # Django detected existing tables
```

OR Django might say:
```
The following models are already created:
  inventory.Category
  inventory.Supplier
  inventory.Product
  inventory.Transaction
```

### When Some Migrations Are Missing:
```bash
$ python manage.py migrate

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, inventory, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying inventory.0001_initial... OK     # Only runs what's missing
```

---

## In Your Specific Situation

Since you **created tables manually** using SQL scripts:

### What Happens:
1. **Django checks** `django_migrations` table
2. **Django checks** if tables exist in database
3. **Django finds** that tables already exist
4. **Django marks** migrations as "applied" without recreating tables
5. **Result:** Django now knows about your tables!

### Why This Is Important:
- Django's ORM (Object-Relational Mapping) needs to know which tables exist
- The `django_migrations` table tracks this
- Without running `migrate`, Django doesn't know your tables exist
- That's why your healthcheck was failing!

---

## What Gets Created/Updated

### Database Tables:
- `django_migrations` - Tracks which migrations ran (Django's internal)
- `auth_user`, `auth_group`, etc. - Django's authentication system
- `inventory_category` - Product categories
- `inventory_supplier` - Suppliers
- `inventory_product` - Products
- `inventory_transaction` - Stock transactions
- Plus other Django system tables

### Database Structure:
- Primary keys
- Foreign key relationships
- Indexes (for performance)
- Constraints (data validation rules)

---

## Common Migrate Commands

```bash
# Apply all pending migrations
python manage.py migrate

# Apply migrations for a specific app only
python manage.py migrate inventory

# Show which migrations are pending/applied
python manage.py showmigrations

# Rollback last migration (undo)
python manage.py migrate inventory 0001

# Fake a migration (mark as applied without running)
python manage.py migrate --fake

# Skip system checks (if checks are failing)
python manage.py migrate --skip-checks
```

---

## Important Notes

### ✅ Safe to Run Multiple Times
- `migrate` is **idempotent** - running it multiple times is safe
- Django only applies migrations that haven't been run
- Won't recreate existing tables

### ✅ Detects Existing Tables
- If tables already exist, Django won't try to recreate them
- Will just mark migrations as applied
- Perfect for your situation!

### ✅ Handles Schema Changes
- If you change a model later, you need to:
  1. `python manage.py makemigrations` (create migration file)
  2. `python manage.py migrate` (apply changes)

### ❌ Not for Creating Admin Users
- `migrate` only handles database schema
- Creating admin users is separate: `python manage.py createsuperuser`

---

## Real-World Example

### Scenario: You Added a New Field

1. **You edit** `inventory/models.py`:
   ```python
   class Product(models.Model):
       # ... existing fields ...
       new_field = models.CharField(max_length=100)  # NEW!
   ```

2. **Create migration file:**
   ```bash
   python manage.py makemigrations
   # Creates: inventory/migrations/0002_add_new_field.py
   ```

3. **Apply to database:**
   ```bash
   python manage.py migrate
   # Runs: ALTER TABLE inventory_product ADD COLUMN new_field VARCHAR(100);
   ```

---

## Summary

`python manage.py migrate` = **"Sync my database with my code models"**

It:
- ✅ Creates missing tables
- ✅ Adds missing columns
- ✅ Updates indexes and constraints
- ✅ Tracks what's been done
- ✅ Is safe to run multiple times
- ✅ Detects existing tables (your case!)

Think of it as Django's way of saying: *"Let me make sure my database matches what my code expects."*

---

## For Your Situation Right Now

Since you created tables manually:

```bash
python manage.py migrate
```

Will:
1. Detect that `inventory_product`, `inventory_category`, etc. already exist
2. Verify their structure matches your models
3. Mark migrations as applied in `django_migrations` table
4. Make Django's ORM aware of these tables
5. Fix your healthcheck endpoint! ✅

That's it! No tables will be recreated, Django just learns about them.

