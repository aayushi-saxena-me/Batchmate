# SQL Scripts for Database Setup

This directory contains SQL scripts to manually create the necessary database tables for the Inventory Management System.

## Files

- **`create_tables_postgresql.sql`** - For PostgreSQL databases (recommended for production)
- **`create_tables_mysql.sql`** - For MySQL/MariaDB databases

## Prerequisites

Before running these scripts, ensure:

1. **Django auth tables exist**: The Django `auth_user` table must be created first. If you're using Django migrations, the auth tables are typically created automatically. You can verify by running:
   ```bash
   python manage.py migrate auth
   ```

2. **Database connection**: Make sure you have proper database credentials and permissions to create tables.

3. **Database exists**: The target database should already be created.

## Usage

### PostgreSQL (Recommended for Production)

```bash
# Method 1: Using psql command line
psql -U your_username -d your_database_name -f create_tables_postgresql.sql

# Method 2: Using psql interactively
psql -U your_username -d your_database_name
\i create_tables_postgresql.sql

# Method 3: From Railway/Render CLI or database admin panel
# Copy and paste the contents of create_tables_postgresql.sql into your database console
```

### MySQL/MariaDB

```bash
# Method 1: Using mysql command line
mysql -u your_username -p your_database_name < create_tables_mysql.sql

# Method 2: Using mysql interactively
mysql -u your_username -p your_database_name
source create_tables_mysql.sql;

# Method 3: From database admin panel (phpMyAdmin, MySQL Workbench, etc.)
# Copy and paste the contents of create_tables_mysql.sql into your SQL console
```

## Tables Created

The scripts create the following tables:

1. **`inventory_category`** - Product categories
   - Fields: id, name (unique), description, created_at, updated_at

2. **`inventory_supplier`** - Supplier/vendor information
   - Fields: id, name, contact_person, email, phone, address, created_at, updated_at

3. **`inventory_product`** - Product inventory information
   - Fields: id, name, description, sku (unique), category_id, supplier_id, quantity, reorder_level, cost_price, selling_price, image, created_by_id, created_at, updated_at, is_active
   - Foreign keys to: inventory_category, inventory_supplier, auth_user
   - Indexes on: sku, name

4. **`inventory_transaction`** - Inventory movement transactions
   - Fields: id, product_id, transaction_type (IN/OUT/ADJUST/RETURN), quantity, reference, notes, created_by_id, created_at
   - Foreign keys to: inventory_product, auth_user
   - Indexes on: product_id + created_at (composite)

## Important Notes

⚠️ **Warning**: These scripts are provided as an alternative to Django migrations. If possible, prefer using Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Django migrations are recommended because they:
- Track migration history
- Handle schema changes automatically
- Are database-agnostic
- Maintain consistency across environments

## When to Use These Scripts

Use these SQL scripts when:
- Django migrations are not available or cannot be run
- You need to set up the database manually on a server
- You're doing a fresh database setup without access to Django
- You want to understand the exact SQL structure

## Verification

After running the scripts, you can verify the tables were created:

### PostgreSQL:
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name LIKE 'inventory_%'
ORDER BY table_name;
```

### MySQL:
```sql
SHOW TABLES LIKE 'inventory_%';
```

## Troubleshooting

### Error: relation "auth_user" does not exist
**Solution**: Run Django auth migrations first:
```bash
python manage.py migrate auth
```

### Error: permission denied
**Solution**: Ensure your database user has CREATE TABLE permissions.

### Error: table already exists
**Solution**: The scripts use `CREATE TABLE IF NOT EXISTS`, so existing tables won't cause errors. If you need to recreate, drop tables first:
```sql
DROP TABLE IF EXISTS inventory_transaction CASCADE;
DROP TABLE IF EXISTS inventory_product CASCADE;
DROP TABLE IF EXISTS inventory_supplier CASCADE;
DROP TABLE IF EXISTS inventory_category CASCADE;
```

## Database-Specific Considerations

### PostgreSQL
- Uses `BIGSERIAL` for auto-incrementing IDs
- Uses `NUMERIC` for decimal fields
- Uses `TIMESTAMP WITH TIME ZONE` for datetime fields
- Supports CHECK constraints for data validation

### MySQL
- Uses `BIGINT AUTO_INCREMENT` for auto-incrementing IDs
- Uses `DECIMAL` for decimal fields
- Uses `TIMESTAMP` for datetime fields
- Uses `INT UNSIGNED` for quantity fields
- CHECK constraints require MySQL 8.0.16+ (earlier versions ignore them)

## Next Steps

After creating the tables:
1. Verify all tables exist and have correct structure
2. Run Django migrations (if using Django) to ensure consistency
3. Create initial data if needed (categories, suppliers, etc.)
4. Test the application

