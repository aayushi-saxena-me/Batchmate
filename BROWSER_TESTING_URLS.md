# Browser Testing URLs Guide

## Starting the Server

First, start your Django development server:

```bash
python manage.py runserver
```

This will start the server at: **http://127.0.0.1:8000/**

---

## All Available URLs

### 🔐 Authentication (No Login Required)

| URL | Description | Purpose |
|-----|-------------|---------|
| `http://127.0.0.1:8000/accounts/login/` | Login page | User login |
| `http://127.0.0.1:8000/accounts/register/` | Registration page | Create new user account |
| `http://127.0.0.1:8000/health/` | Health check | Check if app is running (no login needed) |

### 📊 Dashboard & Main Pages (Login Required)

| URL | Description | What to Test |
|-----|-------------|--------------|
| `http://127.0.0.1:8000/` | Dashboard | Main overview, see only YOUR data |
| `http://127.0.0.1:8000/products/` | Product list | See only YOUR products |
| `http://127.0.0.1:8000/categories/` | Category list | See only YOUR categories |
| `http://127.0.0.1:8000/suppliers/` | Supplier list | See only YOUR suppliers |

### ➕ Create/Add Pages (Login Required)

| URL | Description | What to Test |
|-----|-------------|--------------|
| `http://127.0.0.1:8000/products/add/` | Add product | Form should show only YOUR categories/suppliers |
| `http://127.0.0.1:8000/categories/add/` | Add category | Create category tied to YOUR account |
| `http://127.0.0.1:8000/suppliers/add/` | Add supplier | Create supplier tied to YOUR account |
| `http://127.0.0.1:8000/transactions/add/` | Add transaction | Form should show only YOUR products |

### ✏️ Edit/Detail Pages (Login Required)

| URL | Description | What to Test |
|-----|-------------|--------------|
| `http://127.0.0.1:8000/products/1/` | Product detail | Should only show YOUR products (404 if not yours) |
| `http://127.0.0.1:8000/products/1/edit/` | Edit product | Should only edit YOUR products |
| `http://127.0.0.1:8000/products/1/delete/` | Delete product | Should only delete YOUR products |

### 🔧 Admin Panel (Login Required - Superuser)

| URL | Description | What to Test |
|-----|-------------|--------------|
| `http://127.0.0.1:8000/admin/` | Django admin | Should filter by user, show only YOUR data |

---

## Step-by-Step Testing Guide

### Step 1: Start Server

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### Step 2: Health Check (No Login)

Open: **http://127.0.0.1:8000/health/**

**Expected:**
- ✅ JSON response with status
- ✅ Table existence check
- ✅ No login required

### Step 3: Registration

Open: **http://127.0.0.1:8000/accounts/register/**

**Actions:**
1. Create a new user account
2. Fill in username, email, password
3. Submit form

**Expected:**
- ✅ Redirects to login after registration
- ✅ New user created in database

### Step 4: Login

Open: **http://127.0.0.1:8000/accounts/login/**

**Actions:**
1. Enter username and password
2. Click "Login"

**Expected:**
- ✅ Redirects to dashboard (`/`)
- ✅ Shows your username in navigation
- ✅ No errors

### Step 5: Test Dashboard

Open: **http://127.0.0.1:8000/**

**What to Check:**
- ✅ Shows total products (your products only)
- ✅ Shows low stock alerts (your products only)
- ✅ Shows recent transactions (your transactions only)
- ✅ Charts show only your data

### Step 6: Create Categories

Open: **http://127.0.0.1:8000/categories/add/**

**Actions:**
1. Create a category: "Electronics"
2. Create another: "Clothing"

**Expected:**
- ✅ Categories saved successfully
- ✅ Redirects to categories list
- ✅ Shows success message

### Step 7: Create Suppliers

Open: **http://127.0.0.1:8000/suppliers/add/**

**Actions:**
1. Create supplier: "Tech Supplier"
2. Create another: "Fashion Supplier"

**Expected:**
- ✅ Suppliers saved
- ✅ Appear in suppliers list

### Step 8: Create Products

Open: **http://127.0.0.1:8000/products/add/**

**What to Test:**
- ✅ Category dropdown shows ONLY "Electronics" and "Clothing" (your categories)
- ✅ Supplier dropdown shows ONLY "Tech Supplier" and "Fashion Supplier" (your suppliers)
- ✅ Create product: "Laptop", SKU: "LAP001", quantity: 10

**Expected:**
- ✅ Product created successfully
- ✅ Appears in products list

### Step 9: Test Product List

Open: **http://127.0.0.1:8000/products/**

**What to Check:**
- ✅ Shows only your products
- ✅ Product cards display correctly
- ✅ Search/filter works (if implemented)
- ✅ Links to detail/edit work

### Step 10: Test Product Detail

Click on a product from the list, or go to: **http://127.0.0.1:8000/products/1/**

**What to Check:**
- ✅ Shows product details
- ✅ Shows transaction history (your transactions only)
- ✅ Edit/Delete buttons visible

### Step 11: Test Transaction Creation

Open: **http://127.0.0.1:8000/transactions/add/**

**What to Test:**
- ✅ Product dropdown shows ONLY your products
- ✅ Create a transaction: Stock In, 5 units

**Expected:**
- ✅ Transaction created
- ✅ Product quantity updated
- ✅ Shows in product's transaction history

### Step 12: Test User Isolation

**Create Second User:**
1. Logout (click logout or go to `/accounts/logout/`)
2. Register new user: `http://127.0.0.1:8000/accounts/register/`
3. Create username: "user2", password: "testpass123"
4. Login as user2

**As User2:**
1. Go to: `http://127.0.0.1:8000/products/`
   - ✅ Should be EMPTY (no products from user1)
   
2. Go to: `http://127.0.0.1:8000/categories/`
   - ✅ Should be EMPTY (no categories from user1)
   
3. Go to: `http://127.0.0.1:8000/products/add/`
   - ✅ Category dropdown should be EMPTY
   - ✅ Supplier dropdown should be EMPTY
   - ✅ Create a category first: "Furniture"
   - ✅ Create a product: "Chair", SKU: "CHAIR001"
   
4. Go to: `http://127.0.0.1:8000/products/`
   - ✅ Should see ONLY "Chair" (user2's product)
   - ✅ Should NOT see "Laptop" (user1's product)

**Switch Back to User1:**
1. Logout
2. Login as user1
3. Go to: `http://127.0.0.1:8000/products/`
   - ✅ Should see ONLY "Laptop" (user1's product)
   - ✅ Should NOT see "Chair" (user2's product)

### Step 13: Test Admin Panel

Open: **http://127.0.0.1:8000/admin/**

**Requirements:** Must be a superuser (created with `createsuperuser`)

**What to Check:**
1. Login as superuser
2. Navigate to Inventory → Products
   - ✅ Should see "Created by" column
   - ✅ Should see filter by "Created by"
   - ✅ Should see only YOUR products (or all if superuser)
3. Navigate to Inventory → Categories
   - ✅ Should filter by user
4. Create a new product in admin
   - ✅ Should be assigned to your user automatically

### Step 14: Test Unique Constraints

**As User1:**
1. Go to: `http://127.0.0.1:8000/categories/add/`
2. Try to create category: "Electronics" (duplicate name)
   - ✅ Should show error: "Category with this Name and Created by already exists"

**As User2:**
1. Go to: `http://127.0.0.1:8000/categories/add/`
2. Try to create category: "Electronics" (same name as user1)
   - ✅ Should SUCCEED (different user, so allowed)

**Test SKU Uniqueness:**
1. As User1: Create product with SKU "LAP001" (if already exists, try different)
2. Try to create another product with same SKU "LAP001"
   - ✅ Should show error: "Product with this SKU and Created by already exists"

---

## Quick Test Checklist

### Authentication
- [ ] Can access `/health/` without login
- [ ] Can register new user
- [ ] Can login
- [ ] Can logout
- [ ] Redirected to login if not authenticated

### Data Isolation
- [ ] User1 sees only their products
- [ ] User2 sees only their products
- [ ] User1 cannot see User2's data
- [ ] User2 cannot see User1's data

### Forms
- [ ] Product form shows only user's categories
- [ ] Product form shows only user's suppliers
- [ ] Transaction form shows only user's products

### Constraints
- [ ] Cannot create duplicate category name (same user)
- [ ] Can create same category name (different users)
- [ ] Cannot create duplicate SKU (same user)
- [ ] Can create same SKU (different users)

### CRUD Operations
- [ ] Can create category
- [ ] Can create supplier
- [ ] Can create product
- [ ] Can create transaction
- [ ] Can view product detail
- [ ] Can edit product
- [ ] Can delete product (if implemented)

---

## Common Issues & Solutions

### "Page not found (404)"
- **Check:** Are you logged in? Most pages require authentication.
- **Check:** Does the product/category exist and belong to you?

### "Forbidden (403)"
- **Check:** Are you trying to access another user's data?
- **Expected:** Should get 404 or redirect, not 403

### Forms show all data instead of filtered
- **Check:** Migration ran successfully?
- **Check:** Forms are filtering by `request.user`?

### Categories/Suppliers dropdown empty
- **Check:** Have you created categories/suppliers for this user?
- **Check:** Are you logged in as the correct user?

---

## Testing URLs Summary

**Base URL:** `http://127.0.0.1:8000`

### Must Test These:
1. `/accounts/register/` - Registration
2. `/accounts/login/` - Login
3. `/` - Dashboard
4. `/products/` - Product list
5. `/products/add/` - Add product (test form filtering)
6. `/categories/add/` - Add category
7. `/suppliers/add/` - Add supplier
8. `/transactions/add/` - Add transaction (test form filtering)
9. `/admin/` - Admin panel (if superuser)

### Test with Multiple Users:
1. Create user1 → Create data → Verify
2. Logout → Create user2 → Verify empty lists
3. Create data for user2 → Verify isolation
4. Login as user1 → Verify still only sees user1's data

---

## Next Steps After Testing

If all tests pass:
- ✅ User isolation is working
- ✅ Forms are filtering correctly
- ✅ Constraints work per user
- ✅ Ready for production

If tests fail:
- Check migration ran: `python manage.py migrate inventory`
- Check views filter by user
- Check forms filter choices
- Review error messages

