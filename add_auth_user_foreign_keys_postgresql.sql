-- Add auth_user Foreign Keys - PostgreSQL
-- Run this script AFTER auth_user table has been created (e.g., via Django migrations)
-- This script adds the foreign key constraints to auth_user for inventory tables

BEGIN;

-- Check if auth_user table exists
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'auth_user') THEN
        RAISE EXCEPTION 'auth_user table does not exist. Please create it first using Django migrations: python manage.py migrate auth';
    END IF;
END $$;

-- Add foreign key for inventory_product.created_by_id
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'inventory_product_created_by_id_fk'
    ) THEN
        ALTER TABLE inventory_product
        ADD CONSTRAINT inventory_product_created_by_id_fk 
        FOREIGN KEY (created_by_id) 
        REFERENCES auth_user(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: inventory_product_created_by_id_fk';
    ELSE
        RAISE NOTICE 'Foreign key inventory_product_created_by_id_fk already exists. Skipping.';
    END IF;
END $$;

-- Add foreign key for inventory_transaction.created_by_id
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint 
        WHERE conname = 'inventory_transaction_created_by_id_fk'
    ) THEN
        ALTER TABLE inventory_transaction
        ADD CONSTRAINT inventory_transaction_created_by_id_fk 
        FOREIGN KEY (created_by_id) 
        REFERENCES auth_user(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE;
        
        RAISE NOTICE 'Added foreign key: inventory_transaction_created_by_id_fk';
    ELSE
        RAISE NOTICE 'Foreign key inventory_transaction_created_by_id_fk already exists. Skipping.';
    END IF;
END $$;

COMMIT;

-- Verification
SELECT 
    conname AS constraint_name,
    conrelid::regclass AS table_name
FROM pg_constraint
WHERE conname IN (
    'inventory_product_created_by_id_fk',
    'inventory_transaction_created_by_id_fk'
);

