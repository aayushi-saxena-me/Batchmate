# Quick Start Guide

Get your inventory management system up and running in 5 minutes!

## Quick Commands

```bash
# 1. Activate virtual environment (if not already)
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # macOS/Linux

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Create database tables (first time only)
python manage.py migrate

# 4. Create admin user (first time only)
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

Then open http://127.0.0.1:8000/ in your browser!

## Common Tasks

### Add a Product
1. Login → Products → Add Product
2. Fill in details (Name, SKU, Quantity, Prices)
3. Save

### Process Stock Transaction
1. Go to Product Detail page
2. Click "Transaction" button
3. Select type (Stock In/Out/Adjustment)
4. Enter quantity
5. Process

### View Dashboard
- Shows total products, low stock alerts, and recent activity
- Access from sidebar → Dashboard

### Access Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Use your superuser credentials

## Need More Help?

See `SETUP_GUIDE.md` for detailed instructions and troubleshooting.

