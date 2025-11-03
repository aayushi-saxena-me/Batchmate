-- Assign Existing Data to User - PostgreSQL
-- Run this BEFORE running Django migrations if you have existing data
-- Replace USER_ID with the actual user ID (usually 1 for first user)

-- Step 1: Check if you have users
SELECT id, username FROM auth_user LIMIT 1;

-- Step 2: Get your user ID (replace with your username)
-- SELECT id FROM auth_user WHERE username = 'your_username';

-- Step 3: Add created_by_id columns if they don't exist (safe - won't error if exists)
ALTER TABLE inventory_category 
ADD COLUMN IF NOT EXISTS created_by_id INTEGER;

ALTER TABLE inventory_supplier 
ADD COLUMN IF NOT EXISTS created_by_id INTEGER;

-- Note: Product and Transaction might already have created_by_id
-- Check first: \d inventory_product

-- Step 4: Assign existing records to first user (replace 1 with your user ID)
-- Get user ID first:
-- SELECT id FROM auth_user ORDER BY id LIMIT 1;

-- Then assign (replace USER_ID with actual ID):
DO $$
DECLARE
    default_user_id INTEGER;
BEGIN
    -- Get first user ID
    SELECT id INTO default_user_id FROM auth_user ORDER BY id LIMIT 1;
    
    IF default_user_id IS NULL THEN
        RAISE EXCEPTION 'No users found. Create a user first: python manage.py createsuperuser';
    END IF;
    
    -- Assign existing data
    UPDATE inventory_category 
    SET created_by_id = default_user_id 
    WHERE created_by_id IS NULL;
    
    UPDATE inventory_supplier 
    SET created_by_id = default_user_id 
    WHERE created_by_id IS NULL;
    
    UPDATE inventory_product 
    SET created_by_id = default_user_id 
    WHERE created_by_id IS NULL;
    
    UPDATE inventory_transaction 
    SET created_by_id = default_user_id 
    WHERE created_by_id IS NULL;
    
    RAISE NOTICE 'Assigned existing records to user ID: %', default_user_id;
END $$;

-- Step 5: Make columns required (after assignment)
ALTER TABLE inventory_category 
ALTER COLUMN created_by_id SET NOT NULL;

ALTER TABLE inventory_supplier 
ALTER COLUMN created_by_id SET NOT NULL;

ALTER TABLE inventory_product 
ALTER COLUMN created_by_id SET NOT NULL;

ALTER TABLE inventory_transaction 
ALTER COLUMN created_by_id SET NOT NULL;

-- Step 6: Add foreign key constraints (if not already exist)
-- Check first if they exist, then add:
DO $$
BEGIN
    -- Category foreign key
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'inventory_category_created_by_id_fk'
    ) THEN
        ALTER TABLE inventory_category
        ADD CONSTRAINT inventory_category_created_by_id_fk 
        FOREIGN KEY (created_by_id) 
        REFERENCES auth_user(id) 
        ON DELETE CASCADE;
    END IF;
    
    -- Supplier foreign key
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'inventory_supplier_created_by_id_fk'
    ) THEN
        ALTER TABLE inventory_supplier
        ADD CONSTRAINT inventory_supplier_created_by_id_fk 
        FOREIGN KEY (created_by_id) 
        REFERENCES auth_user(id) 
        ON DELETE CASCADE;
    END IF;
    
    -- Product foreign key (might need to drop and recreate if exists)
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'inventory_product_created_by_id_fk'
    ) THEN
        ALTER TABLE inventory_product
        ADD CONSTRAINT inventory_product_created_by_id_fk 
        FOREIGN KEY (created_by_id) 
        REFERENCES auth_user(id) 
        ON DELETE CASCADE;
    END IF;
    
    -- Transaction foreign key
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'inventory_transaction_created_by_id_fk'
    ) THEN
        ALTER TABLE inventory_transaction
        ADD CONSTRAINT inventory_transaction_created_by_id_fk 
        FOREIGN KEY (created_by_id) 
        REFERENCES auth_user(id) 
        ON DELETE CASCADE;
    END IF;
END $$;

-- Step 7: Add unique constraints per user
-- Remove old unique constraint on category name if exists
DROP INDEX IF EXISTS inventory_category_name_key;

-- Remove old unique constraint on product sku if exists  
DROP INDEX IF EXISTS inventory_product_sku_key;

-- Add per-user unique constraints
CREATE UNIQUE INDEX IF NOT EXISTS inventory_category_name_created_by_idx 
ON inventory_category(name, created_by_id);

CREATE UNIQUE INDEX IF NOT EXISTS inventory_supplier_name_created_by_idx 
ON inventory_supplier(name, created_by_id);

CREATE UNIQUE INDEX IF NOT EXISTS inventory_product_sku_created_by_idx 
ON inventory_product(sku, created_by_id);

-- Step 8: Add performance indexes
CREATE INDEX IF NOT EXISTS inventory_product_created_by_idx 
ON inventory_product(created_by_id);

CREATE INDEX IF NOT EXISTS inventory_category_created_by_idx 
ON inventory_category(created_by_id);

CREATE INDEX IF NOT EXISTS inventory_supplier_created_by_idx 
ON inventory_supplier(created_by_id);

-- Verification: Check all records have created_by
SELECT 
    'Category' as table_name,
    COUNT(*) as total,
    COUNT(created_by_id) as with_user,
    COUNT(*) - COUNT(created_by_id) as missing_user
FROM inventory_category
UNION ALL
SELECT 
    'Supplier',
    COUNT(*),
    COUNT(created_by_id),
    COUNT(*) - COUNT(created_by_id)
FROM inventory_supplier
UNION ALL
SELECT 
    'Product',
    COUNT(*),
    COUNT(created_by_id),
    COUNT(*) - COUNT(created_by_id)
FROM inventory_product
UNION ALL
SELECT 
    'Transaction',
    COUNT(*),
    COUNT(created_by_id),
    COUNT(*) - COUNT(created_by_id)
FROM inventory_transaction;

