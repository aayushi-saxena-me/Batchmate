# Local Testing Guide

## Setup Status ✓

All dependencies have been installed and verified:
- **Django 5.2.7** - Installed and working
- **Database** - Migrations applied successfully
- **System Check** - Passed with no issues

## Starting the Server

You have several options to start the development server:

### Option 1: Use the test script (Recommended)
```bash
.\start_test_server.bat
```

### Option 2: Use the existing run script
```bash
.\run_server.bat
```

### Option 3: Run directly
```bash
py -3.12 manage.py runserver
```

The server will start at: **http://127.0.0.1:8000**

## Testing the Application

### Step 1: Access the Application

Open your browser and navigate to:
- **Main Application**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

### Step 2: Create a User Account

Since the application requires login, you have two options:

#### Option A: Register a New User
1. Go to http://127.0.0.1:8000/accounts/register/
2. Fill in the registration form:
   - Username
   - Password (must meet Django's requirements)
   - Password confirmation
3. Click "Register"
4. You'll be redirected to the login page

#### Option B: Create a Superuser (Admin Access)
Run this command in a new terminal:
```bash
py -3.12 manage.py createsuperuser
```
Follow the prompts to create an admin account. Then login at:
http://127.0.0.1:8000/admin

### Step 3: Test Key Features

Once logged in, you'll be redirected to the dashboard. Test these features:

1. **Dashboard** (`/`)
   - View inventory overview
   - Check low stock alerts
   - Review recent transactions

2. **Products** (`/products/`)
   - View product list
   - Add new products (`/products/add/`)
   - Edit existing products
   - Delete products

3. **Categories** (`/categories/`)
   - View categories
   - Add new categories

4. **Suppliers** (`/suppliers/`)
   - View suppliers
   - Add new suppliers

5. **Transactions** (`/transactions/add/`)
   - Create inventory transactions (stock in/out)

### Step 4: Test Admin Panel

If you created a superuser:
1. Go to http://127.0.0.1:8000/admin
2. Login with your superuser credentials
3. Test managing data through Django's admin interface

## Running the Full Test Suite

To verify everything is working, run:
```bash
.\test_local.bat
```

This will check:
- ✅ Django installation
- ✅ Database migrations
- ✅ Superuser status
- ✅ System configuration

## Troubleshooting

### Port Already in Use
If port 8000 is in use, start the server on a different port:
```bash
py -3.12 manage.py runserver 8001
```

### Database Issues
If you encounter database errors, reset migrations:
```bash
py -3.12 manage.py migrate --run-syncdb
```

### Static Files Not Loading
Collect static files:
```bash
py -3.12 manage.py collectstatic --noinput
```

## Notes

- The server is configured for **development mode** (DEBUG=True)
- Database is **SQLite** (db.sqlite3)
- Media files are served from the `media/` directory
- Static files are served from the `static/` directory

## Next Steps

1. Create test data (products, categories, suppliers)
2. Test CRUD operations for each model
3. Test transaction creation and stock updates
4. Verify dashboard statistics are calculating correctly

