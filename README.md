# Inventory Management System

A comprehensive Django-based inventory management application that allows users to manage their inventory efficiently.

## Features

- **Product Management**: Add, edit, delete, and view products
- **Category Management**: Organize products into categories
- **Supplier Management**: Track suppliers and their information
- **Inventory Tracking**: Monitor stock levels and track transactions
- **User Authentication**: Secure login and registration system
- **Dashboard**: Overview of inventory status and statistics
- **Search & Filter**: Find products quickly with search functionality

## Installation

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser** (admin account):
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the application**:
   - Main app: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
inventory_management/
├── inventory_management/    # Main project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI configuration
├── inventory/               # Inventory app
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── urls.py              # App URLs
│   ├── admin.py             # Admin configuration
│   ├── forms.py             # Forms for data entry
│   └── templates/           # HTML templates
├── accounts/                # Authentication app
│   ├── views.py             # Login/Register views
│   ├── urls.py              # Auth URLs
│   └── templates/           # Auth templates
├── manage.py                # Django management script
└── requirements.txt         # Python dependencies
```

## Usage

### Adding Products
1. Login to your account
2. Navigate to "Products" from the dashboard
3. Click "Add Product"
4. Fill in product details and save

### Managing Inventory
- View all products in the Products list
- Edit product information
- Delete products
- Search and filter products
- View low stock alerts

### Admin Panel
- Access the admin panel with your superuser account
- Manage all models directly
- View detailed reports and analytics

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (default, can be changed to PostgreSQL/MySQL)
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Forms**: Django Crispy Forms

## Development

This is a development version. For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure domain and SSL certificates
5. Set up proper security settings

## License

This project is for educational and personal use.

