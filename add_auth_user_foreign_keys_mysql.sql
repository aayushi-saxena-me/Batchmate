-- Add auth_user Foreign Keys - MySQL
-- Run this script AFTER auth_user table has been created (e.g., via Django migrations)
-- This script adds the foreign key constraints to auth_user for inventory tables

-- First, verify auth_user table exists:
-- SELECT COUNT(*) FROM information_schema.tables 
-- WHERE table_schema = DATABASE() AND table_name = 'auth_user';

-- If the query above returns 0, auth_user doesn't exist yet.
-- Create it first using Django: python manage.py migrate auth

-- Drop existing constraints if they exist (ignore errors if they don't exist)
SET @exist := (SELECT COUNT(*) FROM information_schema.table_constraints 
               WHERE constraint_schema = DATABASE() 
               AND constraint_name = 'inventory_product_created_by_id_fk');
SET @sqlstmt := IF(@exist > 0, 
    'ALTER TABLE inventory_product DROP FOREIGN KEY inventory_product_created_by_id_fk', 
    'SELECT ''Constraint does not exist''');
PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

SET @exist := (SELECT COUNT(*) FROM information_schema.table_constraints 
               WHERE constraint_schema = DATABASE() 
               AND constraint_name = 'inventory_transaction_created_by_id_fk');
SET @sqlstmt := IF(@exist > 0, 
    'ALTER TABLE inventory_transaction DROP FOREIGN KEY inventory_transaction_created_by_id_fk', 
    'SELECT ''Constraint does not exist''');
PREPARE stmt FROM @sqlstmt;
EXECUTE stmt;
DEALLOCATE PREPARE stmt;

-- Add foreign key for inventory_product.created_by_id
ALTER TABLE inventory_product
ADD CONSTRAINT inventory_product_created_by_id_fk 
FOREIGN KEY (created_by_id) 
REFERENCES auth_user(id) 
ON DELETE SET NULL 
ON UPDATE CASCADE;

-- Add foreign key for inventory_transaction.created_by_id
ALTER TABLE inventory_transaction
ADD CONSTRAINT inventory_transaction_created_by_id_fk 
FOREIGN KEY (created_by_id) 
REFERENCES auth_user(id) 
ON DELETE SET NULL 
ON UPDATE CASCADE;

-- Verification
SELECT 
    CONSTRAINT_NAME,
    TABLE_NAME
FROM information_schema.table_constraints
WHERE constraint_schema = DATABASE()
AND constraint_name IN (
    'inventory_product_created_by_id_fk',
    'inventory_transaction_created_by_id_fk'
);

