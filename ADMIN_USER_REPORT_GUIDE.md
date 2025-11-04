# Admin User Report Dashboard

## Overview

An admin-only dashboard that shows comprehensive statistics about all users in the system, including:
- Number of products, categories, suppliers, and transactions per user
- Active products count
- Low stock alerts
- Total inventory value per user
- Top users by activity

## Access

**URL:** `http://127.0.0.1:8000/admin/user-report/`

**Requirements:** 
- Must be logged in
- Must be a superuser (admin)

## Features

### Summary Cards
- **Total Users** - Count of all users in the system
- **Total Products** - Total products across all users
- **Total Categories** - Total categories across all users
- **Total Suppliers** - Total suppliers across all users

### Top Users Section
- **Top Users by Products** - Shows 5 users with the most products
- **Top Users by Transactions** - Shows 5 users with the most transactions

### Detailed User Table
For each user, displays:
- **Username** - User's login name
- **Email** - User's email address
- **Status** - Superuser, Staff, or User badge; Active/Inactive status
- **Products** - Total number of products created
- **Active Products** - Number of active (non-deleted) products
- **Low Stock** - Number of products below reorder level
- **Categories** - Number of categories created
- **Suppliers** - Number of suppliers created
- **Transactions** - Total number of transactions
- **Inventory Value** - Total value (quantity × cost_price) of user's inventory
- **Joined** - Date when user account was created

## How to Create a Superuser

To access the admin user report, you need to create a superuser account:

```bash
python manage.py createsuperuser
```

You'll be prompted to enter:
- Username
- Email (optional)
- Password (twice)

## Accessing the Report

### Option 1: Via Sidebar (if logged in as superuser)
1. Login as superuser
2. Look for "User Report" link in the sidebar
3. Click it

### Option 2: Direct URL
1. Login as superuser
2. Navigate to: `http://127.0.0.1:8000/admin/user-report/`

### Option 3: From Django Admin
1. Login to Django admin: `http://127.0.0.1:8000/admin/`
2. Use the "User Report" link in the sidebar (if available)

## Security

- ✅ Only superusers can access this page
- ✅ Regular users will be redirected or get a 403 error
- ✅ All data is read-only (display only)
- ✅ No sensitive data is exposed (no passwords, etc.)

## What You'll See

### If You Have Multiple Users:
```
User Report Dashboard
├── Summary Cards (totals)
├── Top Users by Products
├── Top Users by Transactions
└── Detailed User Table (all users with stats)
```

### Example Table Row:
```
Username: john_doe
Email: john@example.com
Status: [User] [Active]
Products: 15
Active Products: 12
Low Stock: 2
Categories: 5
Suppliers: 3
Transactions: 45
Inventory Value: $12,345.67
Joined: Jan 15, 2024
```

## Use Cases

1. **Monitor User Activity** - See which users are most active
2. **Resource Planning** - Understand data distribution across users
3. **Support** - Quickly see user statistics when helping users
4. **Analytics** - Track inventory value and product counts per user
5. **Low Stock Alerts** - See which users have low stock items

## Troubleshooting

### "403 Forbidden" or Redirected
- **Cause:** You're not a superuser
- **Fix:** Create a superuser account or have an admin grant you superuser status

### "Page not found (404)"
- **Cause:** URL might be incorrect
- **Fix:** Use exact URL: `/admin/user-report/`

### Empty Table
- **Cause:** No users in the system yet
- **Fix:** Create some users and have them create data

### No "User Report" Link in Sidebar
- **Cause:** You're not logged in as a superuser
- **Fix:** Login as a superuser account

## Integration with Django Admin

The report is separate from Django's built-in admin but can be accessed alongside it. You can:
- View the report at `/admin/user-report/`
- Access Django admin at `/admin/`
- Both are available to superusers

## Future Enhancements

Potential additions:
- Export to CSV/Excel
- Date range filtering
- User activity timeline
- Growth charts
- User comparison
- Bulk actions

