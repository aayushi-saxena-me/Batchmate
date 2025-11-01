# Django Inventory Management System - Setup Guide

This guide will walk you through setting up and running your Django inventory management application.

## Prerequisites

Before you begin, ensure you have:
- **Python 3.8 or higher** installed on your system
- **pip** (Python package manager)
- A code editor (VS Code, PyCharm, etc.)

## Step-by-Step Setup

### 1. Navigate to Project Directory

Open your terminal/command prompt and navigate to the project directory:

```bash
cd "C:\Z Documents\Kids\Aayushi\Batchmate"
```

### 2. Create Virtual Environment (Recommended)

Creating a virtual environment isolates your project dependencies:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt when activated.

### 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.2+
- django-crispy-forms (for beautiful forms)
- crispy-bootstrap5 (Bootstrap 5 integration)
- Pillow (for image handling)

### 4. Run Database Migrations

Django needs to create the database tables. Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates:
- User authentication tables
- Product, Category, Supplier, and Transaction tables
- All necessary database structure

### 5. Create Superuser (Admin Account)

Create an admin account to access the Django admin panel:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password (twice)

**Remember these credentials!** You'll need them to login.

### 6. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

You should see output like:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### 7. Access the Application

Open your web browser and navigate to:

- **Main Application**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## First Steps After Setup

### 1. Login to the Application

- Go to http://127.0.0.1:8000/
- Click "Register" to create a user account, or
- Use your superuser credentials to login

### 2. Create Categories

Before adding products, it's helpful to create categories:
1. Navigate to "Categories" in the sidebar
2. Click "Add Category"
3. Enter category name and description
4. Save

### 3. Add Suppliers

Add supplier information:
1. Navigate to "Suppliers"
2. Click "Add Supplier"
3. Fill in supplier details
4. Save

### 4. Add Your First Product

1. Go to "Products" → "Add Product"
2. Fill in product information:
   - Name, SKU, Description
   - Select Category and Supplier
   - Set initial Quantity and Reorder Level
   - Enter Cost Price and Selling Price
   - Upload an image (optional)
3. Click "Save Product"

### 5. Process Transactions

Track inventory changes:
1. Go to a product detail page
2. Click "Transaction" button
3. Select transaction type:
   - **Stock In**: Adding inventory
   - **Stock Out**: Removing inventory
   - **Adjustment**: Correcting stock levels
   - **Return**: Returning products
4. Enter quantity (negative for OUT, positive for IN)
5. Add reference number and notes
6. Process

## Application Features

### Dashboard
- Overview of inventory statistics
- Low stock alerts
- Recent transactions
- Total inventory value

### Product Management
- View all products with search and filters
- Add, edit, and delete products
- Track stock levels
- View transaction history
- Product images support

### Categories & Suppliers
- Organize products by categories
- Manage supplier information

### Transaction Tracking
- Record all inventory movements
- Automatic stock level updates
- Transaction history per product

## Troubleshooting

### "No module named 'django'"
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### "Table doesn't exist" errors
- Run migrations: `python manage.py migrate`

### Port 8000 already in use
- Use a different port: `python manage.py runserver 8001`

### Images not displaying
- Ensure `media/` directory exists in project root
- Check MEDIA_ROOT and MEDIA_URL in settings.py

## Next Steps & Customization

### Database Configuration
By default, the app uses SQLite. For production, switch to PostgreSQL or MySQL:
1. Update `DATABASES` in `settings.py`
2. Install database adapter (e.g., `psycopg2` for PostgreSQL)
3. Update `requirements.txt`

### Adding More Features
- Reports and Analytics
- Barcode scanning
- Email notifications for low stock
- Multi-location inventory
- Purchase orders
- Sales tracking

### Security Considerations
Before deploying to production:
1. Set `DEBUG = False` in `settings.py`
2. Generate a new `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Set up proper static file serving
5. Use HTTPS
6. Implement additional security middleware

## Getting Help

If you encounter issues:
1. Check Django documentation: https://docs.djangoproject.com/
2. Review error messages in the terminal
3. Check Django logs for detailed error information

## Project Structure Reference

```
Batchmate/
├── inventory_management/     # Main project
│   ├── settings.py            # Configuration
│   ├── urls.py                # Main URLs
│   └── wsgi.py                # WSGI config
├── inventory/                 # Inventory app
│   ├── models.py              # Database models
│   ├── views.py               # View functions
│   ├── urls.py                # App URLs
│   ├── forms.py               # Forms
│   └── templates/             # HTML templates
├── accounts/                  # Authentication app
│   ├── views.py               # Login/Register
│   └── templates/             # Auth templates
├── templates/                 # Base templates
├── static/                    # Static files (CSS, JS, images)
├── media/                     # Uploaded files
├── manage.py                  # Django management
└── requirements.txt           # Dependencies
```

Happy inventory managing! 🎉

