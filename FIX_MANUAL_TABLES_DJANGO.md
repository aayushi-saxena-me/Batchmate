# Fix: Tables Created Manually but Django Doesn't See Them

## Problem
You created tables manually using SQL scripts, and they exist in the database, but Django's healthcheck still says "no such table: inventory_product".

## Root Cause
Django uses the `django_migrations` table to track which migrations have been applied. When you create tables manually, Django doesn't know about them until you either:
1. Run Django migrations (Django will detect existing tables and mark migrations as applied)
2. Manually insert records into `django_migrations` table

## Solution: Run Django Migrations

Even though tables exist, Django needs to know about them. Run migrations - Django will detect existing tables and work with them:

```bash
python manage.py migrate
```

If Django sees tables already exist, it will:
- Check table structure matches
- Mark migrations as applied in `django_migrations` table
- Not try to recreate them

## Alternative: Mark Migrations as Applied Manually

If migrations fail for some reason, you can manually mark them as applied:

### For PostgreSQL:
```sql
-- Check what migrations Django thinks exist
SELECT * FROM django_migrations WHERE app = 'inventory';

-- If inventory migrations are missing, insert them:
INSERT INTO django_migrations (app, name, applied)
VALUES 
    ('inventory', '0001_initial', NOW())
ON CONFLICT DO NOTHING;
```

### Then verify:
```bash
python manage.py migrate --fake
```

This tells Django "these migrations are already applied" without running them.

## Verify the Fix

1. **Check healthcheck endpoint:**
   - Visit: `/health/`
   - Should now show `"status": "healthy"` for `database_tables`

2. **Test ORM access:**
   ```bash
   python manage.py shell
   ```
   ```python
   from inventory.models import Product
   Product.objects.count()  # Should work without error
   ```

## Why This Happens

Django's ORM requires:
1. Tables to exist in database ✅ (you have this)
2. Django to know about them via `django_migrations` table ❌ (missing this)

The improved healthcheck will now:
- First check if tables exist using raw SQL
- Then try ORM access
- Give you better error messages if something is wrong

## Quick Test

After running migrations, test in Django shell:
```python
python manage.py shell
>>> from inventory.models import Product, Category, Supplier
>>> Product.objects.all()  # Should work
>>> Category.objects.all()  # Should work
>>> Supplier.objects.all()  # Should work
```

If these work, your healthcheck should be healthy!

