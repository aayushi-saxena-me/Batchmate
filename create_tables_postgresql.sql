-- PostgreSQL Database Schema for Inventory Management System
-- This script creates all necessary tables for the Django Inventory Management application
-- This version creates tables without auth_user foreign keys first, then adds them separately

BEGIN;

-- ============================================================================
-- 1. CATEGORY TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_category (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add comment to table
COMMENT ON TABLE inventory_category IS 'Product categories';

-- ============================================================================
-- 2. SUPPLIER TABLE
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_supplier (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(254),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add comment to table
COMMENT ON TABLE inventory_supplier IS 'Supplier/vendor information';

-- ============================================================================
-- 3. PRODUCT TABLE (Created without auth_user foreign key - added later)
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_product (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    sku VARCHAR(50) NOT NULL UNIQUE,
    category_id BIGINT,
    supplier_id BIGINT,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    reorder_level INTEGER NOT NULL DEFAULT 10 CHECK (reorder_level >= 0),
    cost_price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    selling_price NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    image VARCHAR(100),
    created_by_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
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
        ON UPDATE CASCADE
);

-- Add comments
COMMENT ON TABLE inventory_product IS 'Product inventory information';
COMMENT ON COLUMN inventory_product.sku IS 'Stock Keeping Unit';
COMMENT ON COLUMN inventory_product.quantity IS 'Current stock quantity';
COMMENT ON COLUMN inventory_product.reorder_level IS 'Alert when stock falls below this level';

-- Create indexes for Product table
CREATE INDEX IF NOT EXISTS inventory_product_sku_idx ON inventory_product(sku);
CREATE INDEX IF NOT EXISTS inventory_product_name_idx ON inventory_product(name);
CREATE INDEX IF NOT EXISTS inventory_product_category_id_idx ON inventory_product(category_id);
CREATE INDEX IF NOT EXISTS inventory_product_supplier_id_idx ON inventory_product(supplier_id);

-- ============================================================================
-- 4. TRANSACTION TABLE (Created without auth_user foreign key - added later)
-- ============================================================================
CREATE TABLE IF NOT EXISTS inventory_transaction (
    id BIGSERIAL PRIMARY KEY,
    product_id BIGINT NOT NULL,
    transaction_type VARCHAR(10) NOT NULL CHECK (transaction_type IN ('IN', 'OUT', 'ADJUST', 'RETURN')),
    quantity INTEGER NOT NULL,
    reference VARCHAR(100),
    notes TEXT,
    created_by_id INTEGER,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign key constraints (auth_user FK added separately below)
    CONSTRAINT inventory_transaction_product_id_fk 
        FOREIGN KEY (product_id) 
        REFERENCES inventory_product(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

-- Add comments
COMMENT ON TABLE inventory_transaction IS 'Inventory movement transactions';
COMMENT ON COLUMN inventory_transaction.transaction_type IS 'Transaction type: IN (Stock In), OUT (Stock Out), ADJUST (Adjustment), RETURN (Return)';

-- Create composite index for Transaction table
CREATE INDEX IF NOT EXISTS inventory_transaction_product_created_at_idx 
    ON inventory_transaction(product_id, created_at DESC);

CREATE INDEX IF NOT EXISTS inventory_transaction_transaction_type_idx 
    ON inventory_transaction(transaction_type);

CREATE INDEX IF NOT EXISTS inventory_transaction_created_at_idx 
    ON inventory_transaction(created_at);

-- ============================================================================
-- ADD AUTH_USER FOREIGN KEYS (Only if auth_user table exists)
-- ============================================================================
-- These constraints are added separately to avoid errors if auth_user doesn't exist yet
-- You can run this section after Django auth migrations are complete

DO $$
BEGIN
    -- Check if auth_user table exists before adding foreign key constraints
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'auth_user') THEN
        -- Add foreign key for inventory_product.created_by_id
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
        END IF;
        
        -- Add foreign key for inventory_transaction.created_by_id
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
        END IF;
        
        RAISE NOTICE 'Foreign key constraints to auth_user have been added successfully.';
    ELSE
        RAISE NOTICE 'auth_user table does not exist. Foreign key constraints to auth_user were not added.';
        RAISE NOTICE 'Run this script again after creating auth_user table (e.g., via Django migrations).';
        RAISE NOTICE 'Or manually add the constraints using the ALTER TABLE statements below.';
    END IF;
END $$;

-- ============================================================================
-- COMMIT TRANSACTION
-- ============================================================================
COMMIT;

-- ============================================================================
-- MANUAL FOREIGN KEY ADDITION (Alternative method)
-- ============================================================================
-- If the automatic foreign key addition above didn't work, you can manually
-- run these commands after auth_user table exists:
--
-- ALTER TABLE inventory_product
-- ADD CONSTRAINT inventory_product_created_by_id_fk 
-- FOREIGN KEY (created_by_id) 
-- REFERENCES auth_user(id) 
-- ON DELETE SET NULL 
-- ON UPDATE CASCADE;
--
-- ALTER TABLE inventory_transaction
-- ADD CONSTRAINT inventory_transaction_created_by_id_fk 
-- FOREIGN KEY (created_by_id) 
-- REFERENCES auth_user(id) 
-- ON DELETE SET NULL 
-- ON UPDATE CASCADE;

-- ============================================================================
-- VERIFICATION QUERIES (Optional - uncomment to verify tables were created)
-- ============================================================================
-- SELECT table_name 
-- FROM information_schema.tables 
-- WHERE table_schema = 'public' 
-- AND table_name LIKE 'inventory_%'
-- ORDER BY table_name;
--
-- SELECT 
--     t.table_name,
--     c.column_name,
--     c.data_type,
--     c.is_nullable
-- FROM information_schema.tables t
-- JOIN information_schema.columns c ON t.table_name = c.table_name
-- WHERE t.table_schema = 'public' 
-- AND t.table_name LIKE 'inventory_%'
-- ORDER BY t.table_name, c.ordinal_position;

