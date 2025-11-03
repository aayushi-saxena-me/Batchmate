# Testing Guide: User Data Isolation

## Overview

This guide helps you test that:
1. ✅ Migration works correctly
2. ✅ Data is isolated per user
3. ✅ Users can only see/edit their own data
4. ✅ Forms show only user's data
5. ✅ Views filter correctly
6. ✅ Admin filters correctly

---

## Prerequisites

Before testing, ensure:
- ✅ Django is installed
- ✅ Database is accessible
- ✅ You can run migrations

---

## Step 1: Test Migration

### 1.1 Check Current State

```bash
python manage.py shell
```

```python
from inventory.models import Category, Supplier, Product, Transaction
from django.contrib.auth.models import User

# Check if users exist
print(f"Users: {User.objects.count()}")

# Check existing data
print(f"Categories: {Category.objects.count()}")
print(f"Suppliers: {Supplier.objects.count()}")
print(f"Products: {Product.objects.count()}")
print(f"Transactions: {Transaction.objects.count()}")

# Check if created_by fields exist (may fail if columns don't exist - that's OK)
try:
    print(f"Categories without user: {Category.objects.filter(created_by__isnull=True).count()}")
except:
    print("Category.created_by column doesn't exist yet (expected)")
```

### 1.2 Create Test User (if needed)

```bash
python manage.py createsuperuser
# Username: admin
# Email: admin@test.com
# Password: testpass123
```

### 1.3 Run Migration

```bash
python manage.py migrate inventory
```

**Expected output:**
```
Operations to perform:
  Apply all migrations: inventory
Running migrations:
  Applying inventory.0002_add_user_isolation... OK
```

### 1.4 Verify Migration

```bash
python manage.py shell
```

```python
from inventory.models import *
from django.contrib.auth.models import User

user = User.objects.first()

# All records should have created_by now
print(f"Categories without user: {Category.objects.filter(created_by__isnull=True).count()}")
print(f"Suppliers without user: {Supplier.objects.filter(created_by__isnull=True).count()}")
print(f"Products without user: {Product.objects.filter(created_by__isnull=True).count()}")
print(f"Transactions without user: {Transaction.objects.filter(created_by__isnull=True).count()}")

# All should be 0!

# Check records assigned to user
print(f"\n{user.username} owns:")
print(f"  Categories: {Category.objects.filter(created_by=user).count()}")
print(f"  Suppliers: {Supplier.objects.filter(created_by=user).count()}")
print(f"  Products: {Product.objects.filter(created_by=user).count()}")
print(f"  Transactions: {Transaction.objects.filter(created_by=user).count()}")
```

---

## Step 2: Test Data Isolation

### 2.1 Create Multiple Users

```bash
python manage.py createsuperuser
# Username: user1
# Email: user1@test.com
# Password: testpass123

python manage.py createsuperuser
# Username: user2
# Email: user2@test.com
# Password: testpass123
```

### 2.2 Create Data for Each User

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction
from decimal import Decimal

# Get users
user1 = User.objects.get(username='user1')
user2 = User.objects.get(username='user2')

# Create data for user1
cat1 = Category.objects.create(name='Electronics', created_by=user1)
sup1 = Supplier.objects.create(name='Tech Supplier', created_by=user1)
prod1 = Product.objects.create(
    name='Laptop',
    sku='LAP001',
    quantity=10,
    cost_price=Decimal('500.00'),
    selling_price=Decimal('800.00'),
    created_by=user1
)

# Create data for user2
cat2 = Category.objects.create(name='Clothing', created_by=user2)
sup2 = Supplier.objects.create(name='Fashion Supplier', created_by=user2)
prod2 = Product.objects.create(
    name='T-Shirt',
    sku='TSH001',
    quantity=20,
    cost_price=Decimal('10.00'),
    selling_price=Decimal('25.00'),
    created_by=user2
)

print("Test data created!")
print(f"User1: {Category.objects.filter(created_by=user1).count()} categories")
print(f"User2: {Category.objects.filter(created_by=user2).count()} categories")
```

### 2.3 Test Views (Manual Testing)

Start server:
```bash
python manage.py runserver
```

**Test Scenario 1: Login as user1**
1. Go to: http://127.0.0.1:8000/accounts/login/
2. Login as `user1` / `testpass123`
3. Navigate to:
   - Dashboard: http://127.0.0.1:8000/
   - Products: http://127.0.0.1:8000/products/
   - Categories: http://127.0.0.1:8000/categories/
   - Suppliers: http://127.0.0.1:8000/suppliers/
4. **Verify:** You should ONLY see:
   - Electronics category
   - Tech Supplier
   - Laptop product
5. **Verify:** You should NOT see:
   - Clothing category
   - Fashion Supplier
   - T-Shirt product

**Test Scenario 2: Login as user2**
1. Logout
2. Login as `user2` / `testpass123`
3. Navigate to same pages
4. **Verify:** You should ONLY see:
   - Clothing category
   - Fashion Supplier
   - T-Shirt product
5. **Verify:** You should NOT see:
   - Electronics category
   - Tech Supplier
   - Laptop product

---

## Step 3: Test Forms

### 3.1 Test Product Form

**As user1:**
1. Login as `user1`
2. Go to: http://127.0.0.1:8000/products/add/ (or edit existing)
3. **Verify in Product Form:**
   - Category dropdown shows ONLY "Electronics" (user1's category)
   - Category dropdown does NOT show "Clothing" (user2's category)
   - Supplier dropdown shows ONLY "Tech Supplier" (user1's supplier)
   - Supplier dropdown does NOT show "Fashion Supplier" (user2's supplier)

**As user2:**
1. Login as `user2`
2. Create/edit a product
3. **Verify:**
   - Category dropdown shows ONLY "Clothing"
   - Category dropdown does NOT show "Electronics"
   - Supplier dropdown shows ONLY "Fashion Supplier"
   - Supplier dropdown does NOT show "Tech Supplier"

### 3.2 Test Transaction Form

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Product

# Create more products for testing
user1 = User.objects.get(username='user1')
user2 = User.objects.get(username='user2')

prod1_user1 = Product.objects.get(sku='LAP001', created_by=user1)
prod2_user2 = Product.objects.get(sku='TSH001', created_by=user2)

print(f"User1 products: {Product.objects.filter(created_by=user1).count()}")
print(f"User2 products: {Product.objects.filter(created_by=user2).count()}")
```

**Test in Browser:**
1. Login as `user1`
2. Go to: http://127.0.0.1:8000/transactions/create/
3. **Verify:**
   - Product dropdown shows ONLY user1's products (Laptop)
   - Product dropdown does NOT show user2's products (T-Shirt)

4. Login as `user2`
5. Go to transactions page
6. **Verify:**
   - Product dropdown shows ONLY user2's products (T-Shirt)
   - Product dropdown does NOT show user1's products (Laptop)

---

## Step 4: Test Admin Interface

### 4.1 Access Admin

1. Go to: http://127.0.0.1:8000/admin/
2. Login as `user1`

### 4.2 Test Admin Filters

**Navigate to:**
- Inventory → Categories
- Inventory → Suppliers
- Inventory → Products
- Inventory → Transactions

**Verify:**
- Each list shows ONLY user1's data
- You can see "Created by" column
- Filter by "Created by" works
- When creating new records, they're automatically assigned to user1

**Test as user2:**
- Login as `user2` in admin
- Verify admin shows ONLY user2's data

---

## Step 5: Test Unique Constraints

### 5.1 Test Per-User Unique Names

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product

user1 = User.objects.get(username='user1')
user2 = User.objects.get(username='user2')

# This should work - same name, different users
Category.objects.create(name='Electronics', created_by=user2)
print("✅ Users can have same category name")

# This should fail - same name, same user
try:
    Category.objects.create(name='Electronics', created_by=user1)
    print("❌ ERROR: Duplicate category name allowed!")
except Exception as e:
    print(f"✅ Correctly prevented duplicate: {e}")
```

### 5.2 Test Per-User Unique SKU

```python
# This should work - same SKU, different users
Product.objects.create(
    name='Laptop Pro',
    sku='LAP001',  # Same SKU as user1's laptop
    quantity=5,
    created_by=user2
)
print("✅ Users can have same SKU")

# This should fail - same SKU, same user
try:
    Product.objects.create(
        name='Laptop 2',
        sku='LAP001',  # Same SKU, same user
        quantity=3,
        created_by=user1
    )
    print("❌ ERROR: Duplicate SKU allowed!")
except Exception as e:
    print(f"✅ Correctly prevented duplicate: {e}")
```

---

## Step 6: Automated Test Script

Create a test script:

```python
# test_user_isolation.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory_management.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Product, Transaction
from decimal import Decimal

def test_user_isolation():
    print("=" * 60)
    print("Testing User Data Isolation")
    print("=" * 60)
    
    # Get or create users
    user1, _ = User.objects.get_or_create(username='testuser1', defaults={'email': 'u1@test.com'})
    user1.set_password('testpass123')
    user1.save()
    
    user2, _ = User.objects.get_or_create(username='testuser2', defaults={'email': 'u2@test.com'})
    user2.set_password('testpass123')
    user2.save()
    
    # Create data for user1
    cat1 = Category.objects.create(name='Test Category 1', created_by=user1)
    sup1 = Supplier.objects.create(name='Test Supplier 1', created_by=user1)
    prod1 = Product.objects.create(
        name='Test Product 1',
        sku='TEST001',
        quantity=10,
        created_by=user1
    )
    
    # Create data for user2
    cat2 = Category.objects.create(name='Test Category 2', created_by=user2)
    sup2 = Supplier.objects.create(name='Test Supplier 2', created_by=user2)
    prod2 = Product.objects.create(
        name='Test Product 2',
        sku='TEST002',
        quantity=20,
        created_by=user2
    )
    
    # Test 1: Users can't see each other's categories
    user1_cats = Category.objects.filter(created_by=user1)
    user2_cats = Category.objects.filter(created_by=user2)
    
    assert cat1 in user1_cats, "❌ User1 should see their category"
    assert cat2 not in user1_cats, "❌ User1 should NOT see user2's category"
    assert cat2 in user2_cats, "❌ User2 should see their category"
    assert cat1 not in user2_cats, "❌ User2 should NOT see user1's category"
    print("✅ Test 1: Category isolation works")
    
    # Test 2: Users can't see each other's products
    user1_prods = Product.objects.filter(created_by=user1)
    user2_prods = Product.objects.filter(created_by=user2)
    
    assert prod1 in user1_prods, "❌ User1 should see their product"
    assert prod2 not in user1_prods, "❌ User1 should NOT see user2's product"
    print("✅ Test 2: Product isolation works")
    
    # Test 3: Unique constraints per user
    try:
        Category.objects.create(name='Test Category 1', created_by=user1)
        print("❌ Test 3: Duplicate category name should fail!")
    except:
        print("✅ Test 3: Unique category name per user works")
    
    try:
        Product.objects.create(name='New', sku='TEST001', quantity=1, created_by=user1)
        print("❌ Test 3: Duplicate SKU should fail!")
    except:
        print("✅ Test 3: Unique SKU per user works")
    
    # Cleanup
    Transaction.objects.filter(product__in=[prod1, prod2]).delete()
    Product.objects.filter(id__in=[prod1.id, prod2.id]).delete()
    Category.objects.filter(id__in=[cat1.id, cat2.id]).delete()
    Supplier.objects.filter(id__in=[sup1.id, sup2.id]).delete()
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)

if __name__ == '__main__':
    test_user_isolation()
```

Run it:
```bash
python test_user_isolation.py
```

---

## Step 7: Quick Test Checklist

### Pre-Migration
- [ ] Check current data count
- [ ] Create at least one user
- [ ] Note existing records (if any)

### Migration
- [ ] Run `python manage.py migrate inventory`
- [ ] Verify no errors
- [ ] Check all records have `created_by`
- [ ] Verify records assigned to first user

### Post-Migration
- [ ] Create second user
- [ ] Create data for each user
- [ ] Login as user1 → see only user1's data
- [ ] Login as user2 → see only user2's data
- [ ] Test product form → only shows user's categories/suppliers
- [ ] Test transaction form → only shows user's products
- [ ] Test admin → filters by user
- [ ] Test unique constraints → same name/SKU allowed for different users
- [ ] Test unique constraints → same name/SKU fails for same user

---

## Step 8: Test Edge Cases

### 8.1 Test Empty Data

```python
# Create user with no data
user3 = User.objects.create_user('user3', 'u3@test.com', 'pass')

# Login as user3
# Should see empty lists (not errors)
# Should be able to create new data
```

### 8.2 Test Deletion

```python
# User1 deletes their category
# Should cascade to products (if any)
# Should NOT affect user2's data
```

### 8.3 Test Direct Database Access

```bash
python manage.py shell
```

```python
# Try to access another user's data directly (should work in shell)
# But views should filter it out
from inventory.models import Product
from django.contrib.auth.models import User

user1 = User.objects.get(username='user1')
user2 = User.objects.get(username='user2')

# In shell, you CAN see all (because no filter)
all_products = Product.objects.all()
print(f"All products: {all_products.count()}")

# But with filter, you see only user's
user1_products = Product.objects.filter(created_by=user1)
print(f"User1 products: {user1_products.count()}")
```

---

## Troubleshooting

### Migration Fails
- Check: Do you have a user? `python manage.py createsuperuser`
- Check: Are tables created? `python manage.py migrate`

### Can See Other User's Data
- Check: Views filter by `request.user`
- Check: Forms filter by `request.user`
- Check: Migration ran successfully

### Forms Show All Data
- Check: Form `__init__` methods filter choices
- Check: `request.user` is passed correctly

### Admin Shows All Data
- Check: Admin classes have `get_queryset` method
- Check: Admin filters are set up

---

## Summary

**Quick Test:**
1. Create 2 users
2. Create data for each
3. Login as each user
4. Verify isolation

**Full Test:**
- Run all steps above
- Test forms, views, admin
- Test constraints
- Test edge cases

**Expected Result:**
✅ Users can only see/edit their own data
✅ Forms show only user's choices
✅ Unique constraints work per user
✅ No data leakage between users
