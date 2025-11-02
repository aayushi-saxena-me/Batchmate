-- MySQL Database Schema for Inventory Management System
-- This script creates all necessary tables for the Django Inventory Management application
-- This version creates tables without auth_user foreign keys first, then adds them separately

-- Use your database name here
-- USE your_database_name;

-- ============================================================================
-- 1. CATEGORY TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_category (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_category_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. SUPPLIER TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_supplier (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(254),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_supplier_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. PRODUCT TABLE (Created without auth_user foreign key - added later)
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_product (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    sku VARCHAR(50) NOT NULL UNIQUE,
    category_id BIGINT,
    supplier_id BIGINT,
    quantity INT UNSIGNED NOT NULL DEFAULT 0,
    reorder_level INT UNSIGNED NOT NULL DEFAULT 10,
    cost_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    selling_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    image VARCHAR(100),
    created_by_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    
    -- Foreign key constraints (auth_user FK added separately below)
    CONSTRAINT inventory_product_category_id_fk 
        FOREIGN KEY (category_id) 
        REFERENCES inventory_category(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    CONSTRAINT inventory_product_supplier_id_fk 
        FOREIGN KEY (supplier_id) 
        REFERENCES inventory_supplier(id) 
        ON DELETE SET NULL 
        ON UPDATE CASCADE,
    
    -- Indexes
    INDEX inventory_product_sku_idx (sku),
    INDEX inventory_product_name_idx (name),
    INDEX inventory_product_category_id_idx (category_id),
    INDEX inventory_product_supplier_id_idx (supplier_id),
    
    -- Check constraints (MySQL 8.0.16+)
    CONSTRAINT chk_quantity_non_negative CHECK (quantity >= 0),
    CONSTRAINT chk_reorder_level_non_negative CHECK (reorder_level >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. TRANSACTION TABLE (Created without auth_user foreign key - added later)
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_transaction (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    product_id BIGINT NOT NULL,
    transaction_type VARCHAR(10) NOT NULL,
    quantity INT NOT NULL,
    reference VARCHAR(100),
    notes TEXT,
    created_by_id INT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints (auth_user FK added separately below)
    CONSTRAINT inventory_transaction_product_id_fk 
        FOREIGN KEY (product_id) 
        REFERENCES inventory_product(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    -- Indexes
    INDEX inventory_transaction_product_created_at_idx (product_id, created_at DESC),
    INDEX inventory_transaction_transaction_type_idx (transaction_type),
    INDEX inventory_transaction_created_at_idx (created_at),
    
    -- Check constraint for transaction_type (MySQL 8.0.16+)
    CONSTRAINT chk_transaction_type 
        CHECK (transaction_type IN ('IN', 'OUT', 'ADJUST', 'RETURN'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- ADD AUTH_USER FOREIGN KEYS (Only if auth_user table exists)
-- ============================================================================
-- Run these commands AFTER auth_user table has been created (via Django migrations)
-- Check if auth_user exists first, then run the ALTER TABLE statements below

-- Check if auth_user exists (run this query first):
-- SELECT COUNT(*) FROM information_schema.tables 
-- WHERE table_schema = DATABASE() AND table_name = 'auth_user';

-- If auth_user exists, run these ALTER TABLE statements:

ALTER TABLE inventory_product
ADD CONSTRAINT inventory_product_created_by_id_fk 
FOREIGN KEY (created_by_id) 
REFERENCES auth_user(id) 
ON DELETE SET NULL 
ON UPDATE CASCADE;

ALTER TABLE inventory_transaction
ADD CONSTRAINT inventory_transaction_created_by_id_fk 
FOREIGN KEY (created_by_id) 
REFERENCES auth_user(id) 
ON DELETE SET NULL 
ON UPDATE CASCADE;

-- Note: If you get "Duplicate foreign key constraint" error, the constraint already exists.
-- You can safely ignore it or drop it first:
-- ALTER TABLE inventory_product DROP FOREIGN KEY inventory_product_created_by_id_fk;
-- ALTER TABLE inventory_transaction DROP FOREIGN KEY inventory_transaction_created_by_id_fk;

-- ============================================================================
-- VERIFICATION QUERIES (Optional - uncomment to verify tables were created)
-- ============================================================================
-- SHOW TABLES LIKE 'inventory_%';
--
-- SELECT 
--     TABLE_NAME,
--     COLUMN_NAME,
--     DATA_TYPE,
--     IS_NULLABLE
-- FROM INFORMATION_SCHEMA.COLUMNS
-- WHERE TABLE_SCHEMA = DATABASE()
-- AND TABLE_NAME LIKE 'inventory_%'
-- ORDER BY TABLE_NAME, ORDINAL_POSITION;

