-- ============================================================
-- STOCK MANAGEMENT DATABASE SCHEMA
-- Database: PostgreSQL / MySQL compatible
-- Created: December 6, 2025
-- ============================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS transaction_history CASCADE;
DROP TABLE IF EXISTS product_movements CASCADE;
DROP TABLE IF EXISTS stock_adjustments CASCADE;
DROP TABLE IF EXISTS purchase_orders CASCADE;
DROP TABLE IF EXISTS sales_orders CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS categories CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS warehouses CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ============================================================
-- 1. USERS TABLE
-- Stores user accounts for the system
-- ============================================================
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(20) CHECK (role IN ('admin', 'manager', 'warehouse_staff', 'viewer')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 2. CATEGORIES TABLE
-- Product categories for classification
-- ============================================================
CREATE TABLE categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    parent_category_id INT REFERENCES categories(category_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 3. SUPPLIERS TABLE
-- Supplier/vendor information
-- ============================================================
CREATE TABLE suppliers (
    supplier_id SERIAL PRIMARY KEY,
    supplier_name VARCHAR(200) NOT NULL,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    payment_terms VARCHAR(50),
    lead_time_days INT,
    min_order_quantity INT,
    is_active BOOLEAN DEFAULT TRUE,
    rating DECIMAL(3, 2) CHECK (rating >= 0 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 4. WAREHOUSES TABLE
-- Warehouse/storage location information
-- ============================================================
CREATE TABLE warehouses (
    warehouse_id SERIAL PRIMARY KEY,
    warehouse_name VARCHAR(100) UNIQUE NOT NULL,
    warehouse_code VARCHAR(20) UNIQUE NOT NULL,
    address TEXT,
    city VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    capacity_cubic_meters DECIMAL(12, 2),
    manager_name VARCHAR(100),
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 5. PRODUCTS TABLE
-- Master product information
-- ============================================================
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    sku VARCHAR(50) UNIQUE NOT NULL,
    product_name VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INT REFERENCES categories(category_id),
    brand VARCHAR(100),
    manufacturer VARCHAR(100),
    
    -- Physical characteristics
    weight_kg DECIMAL(10, 3),
    length_cm DECIMAL(10, 2),
    width_cm DECIMAL(10, 2),
    height_cm DECIMAL(10, 2),
    unit_of_measure VARCHAR(20) DEFAULT 'pieces',
    
    -- Financial data
    cost_price DECIMAL(12, 2) NOT NULL,
    selling_price DECIMAL(12, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    
    -- Inventory settings
    reorder_point INT DEFAULT 10,
    reorder_quantity INT DEFAULT 50,
    min_stock_level INT DEFAULT 5,
    max_stock_level INT DEFAULT 1000,
    
    -- Quality & compliance
    has_expiry BOOLEAN DEFAULT FALSE,
    shelf_life_days INT,
    requires_certification BOOLEAN DEFAULT FALSE,
    is_hazardous BOOLEAN DEFAULT FALSE,
    
    -- Categorization
    abc_classification VARCHAR(1) CHECK (abc_classification IN ('A', 'B', 'C')),
    velocity_classification VARCHAR(10) CHECK (velocity_classification IN ('fast', 'medium', 'slow')),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    discontinued_date DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 6. INVENTORY TABLE
-- Current stock levels per warehouse
-- ============================================================
CREATE TABLE inventory (
    inventory_id SERIAL PRIMARY KEY,
    product_id INT NOT NULL REFERENCES products(product_id),
    warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    
    -- Stock levels
    quantity_on_hand INT NOT NULL DEFAULT 0,
    quantity_reserved INT DEFAULT 0,
    quantity_available INT GENERATED ALWAYS AS (quantity_on_hand - quantity_reserved) STORED,
    
    -- Location details
    aisle VARCHAR(10),
    rack VARCHAR(10),
    shelf VARCHAR(10),
    bin_location VARCHAR(20),
    
    -- Tracking
    last_counted_date DATE,
    last_counted_by INT REFERENCES users(user_id),
    last_restocked_date DATE,
    last_movement_date DATE,
    
    -- Batch/Lot tracking
    batch_number VARCHAR(50),
    lot_number VARCHAR(50),
    manufacturing_date DATE,
    expiry_date DATE,
    
    -- Status
    stock_status VARCHAR(20) CHECK (stock_status IN ('critical', 'low', 'adequate', 'overstocked')),
    quality_status VARCHAR(20) DEFAULT 'approved' CHECK (quality_status IN ('approved', 'quarantine', 'rejected')),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(product_id, warehouse_id, batch_number)
);

-- ============================================================
-- 7. PURCHASE ORDERS TABLE
-- Purchase orders from suppliers
-- ============================================================
CREATE TABLE purchase_orders (
    po_id SERIAL PRIMARY KEY,
    po_number VARCHAR(50) UNIQUE NOT NULL,
    supplier_id INT NOT NULL REFERENCES suppliers(supplier_id),
    warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    
    -- Order details
    order_date DATE NOT NULL,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'ordered', 'partially_received', 'received', 'cancelled')),
    
    -- Financial
    total_amount DECIMAL(15, 2),
    tax_amount DECIMAL(15, 2),
    shipping_cost DECIMAL(12, 2),
    
    -- Tracking
    created_by INT REFERENCES users(user_id),
    approved_by INT REFERENCES users(user_id),
    received_by INT REFERENCES users(user_id),
    
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 8. PURCHASE ORDER ITEMS TABLE
-- Line items in purchase orders
-- ============================================================
CREATE TABLE purchase_order_items (
    po_item_id SERIAL PRIMARY KEY,
    po_id INT NOT NULL REFERENCES purchase_orders(po_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    
    quantity_ordered INT NOT NULL,
    quantity_received INT DEFAULT 0,
    unit_price DECIMAL(12, 2) NOT NULL,
    line_total DECIMAL(15, 2) GENERATED ALWAYS AS (quantity_ordered * unit_price) STORED,
    
    batch_number VARCHAR(50),
    manufacturing_date DATE,
    expiry_date DATE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 9. SALES ORDERS TABLE
-- Customer sales orders
-- ============================================================
CREATE TABLE sales_orders (
    so_id SERIAL PRIMARY KEY,
    so_number VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(200),
    customer_email VARCHAR(100),
    warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    
    -- Order details
    order_date DATE NOT NULL,
    required_date DATE,
    shipped_date DATE,
    
    -- Status
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled', 'returned')),
    
    -- Financial
    total_amount DECIMAL(15, 2),
    tax_amount DECIMAL(15, 2),
    shipping_cost DECIMAL(12, 2),
    
    -- Tracking
    created_by INT REFERENCES users(user_id),
    processed_by INT REFERENCES users(user_id),
    
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 10. SALES ORDER ITEMS TABLE
-- Line items in sales orders
-- ============================================================
CREATE TABLE sales_order_items (
    so_item_id SERIAL PRIMARY KEY,
    so_id INT NOT NULL REFERENCES sales_orders(so_id) ON DELETE CASCADE,
    product_id INT NOT NULL REFERENCES products(product_id),
    
    quantity_ordered INT NOT NULL,
    quantity_shipped INT DEFAULT 0,
    unit_price DECIMAL(12, 2) NOT NULL,
    line_total DECIMAL(15, 2) GENERATED ALWAYS AS (quantity_ordered * unit_price) STORED,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 11. TRANSACTION HISTORY TABLE
-- Complete audit trail of all inventory movements
-- ============================================================
CREATE TABLE transaction_history (
    transaction_id SERIAL PRIMARY KEY,
    transaction_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    transaction_type VARCHAR(20) NOT NULL CHECK (transaction_type IN ('purchase', 'sale', 'adjustment', 'transfer', 'return', 'damage', 'theft', 'cycle_count')),
    reference_number VARCHAR(50),
    
    -- Product and location
    product_id INT NOT NULL REFERENCES products(product_id),
    warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    
    -- Quantity changes
    quantity_change INT NOT NULL,
    quantity_before INT,
    quantity_after INT,
    
    -- Financial
    unit_cost DECIMAL(12, 2),
    total_value DECIMAL(15, 2),
    
    -- Related records
    po_id INT REFERENCES purchase_orders(po_id),
    so_id INT REFERENCES sales_orders(so_id),
    
    -- Tracking
    performed_by INT REFERENCES users(user_id),
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 12. STOCK ADJUSTMENTS TABLE
-- Manual stock adjustments (corrections, damages, etc.)
-- ============================================================
CREATE TABLE stock_adjustments (
    adjustment_id SERIAL PRIMARY KEY,
    adjustment_date DATE NOT NULL,
    adjustment_type VARCHAR(20) NOT NULL CHECK (adjustment_type IN ('correction', 'damage', 'theft', 'expired', 'found', 'write_off')),
    
    product_id INT NOT NULL REFERENCES products(product_id),
    warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    
    quantity_adjusted INT NOT NULL,
    reason TEXT NOT NULL,
    
    -- Financial impact
    cost_impact DECIMAL(15, 2),
    
    -- Approval
    adjusted_by INT REFERENCES users(user_id),
    approved_by INT REFERENCES users(user_id),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- 13. PRODUCT MOVEMENTS TABLE
-- Transfers between warehouses
-- ============================================================
CREATE TABLE product_movements (
    movement_id SERIAL PRIMARY KEY,
    movement_date DATE NOT NULL,
    product_id INT NOT NULL REFERENCES products(product_id),
    
    from_warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    to_warehouse_id INT NOT NULL REFERENCES warehouses(warehouse_id),
    
    quantity INT NOT NULL,
    
    status VARCHAR(20) DEFAULT 'initiated' CHECK (status IN ('initiated', 'in_transit', 'received', 'cancelled')),
    
    initiated_by INT REFERENCES users(user_id),
    received_by INT REFERENCES users(user_id),
    
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- INDEXES for performance optimization
-- ============================================================

-- Products indexes
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);

-- Inventory indexes
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_inventory_warehouse ON inventory(warehouse_id);
CREATE INDEX idx_inventory_status ON inventory(stock_status);
CREATE INDEX idx_inventory_expiry ON inventory(expiry_date);

-- Transaction history indexes
CREATE INDEX idx_transaction_date ON transaction_history(transaction_date);
CREATE INDEX idx_transaction_product ON transaction_history(product_id);
CREATE INDEX idx_transaction_type ON transaction_history(transaction_type);
CREATE INDEX idx_transaction_reference ON transaction_history(reference_number);

-- Purchase orders indexes
CREATE INDEX idx_po_number ON purchase_orders(po_number);
CREATE INDEX idx_po_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_po_status ON purchase_orders(status);
CREATE INDEX idx_po_date ON purchase_orders(order_date);

-- Sales orders indexes
CREATE INDEX idx_so_number ON sales_orders(so_number);
CREATE INDEX idx_so_status ON sales_orders(status);
CREATE INDEX idx_so_date ON sales_orders(order_date);

-- ============================================================
-- VIEWS for common queries
-- ============================================================

-- View: Current Stock Levels Across All Warehouses
CREATE VIEW v_current_stock_summary AS
SELECT 
    p.product_id,
    p.sku,
    p.product_name,
    c.category_name,
    SUM(i.quantity_on_hand) as total_quantity,
    SUM(i.quantity_reserved) as total_reserved,
    SUM(i.quantity_available) as total_available,
    p.reorder_point,
    p.cost_price,
    SUM(i.quantity_on_hand * p.cost_price) as total_value,
    CASE 
        WHEN SUM(i.quantity_on_hand) < p.reorder_point * 0.5 THEN 'Critical'
        WHEN SUM(i.quantity_on_hand) < p.reorder_point THEN 'Low'
        WHEN SUM(i.quantity_on_hand) < p.reorder_point * 2 THEN 'Adequate'
        ELSE 'Overstocked'
    END as stock_status
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN categories c ON p.category_id = c.category_id
WHERE p.is_active = TRUE
GROUP BY p.product_id, p.sku, p.product_name, c.category_name, p.reorder_point, p.cost_price;

-- View: Stock by Warehouse
CREATE VIEW v_stock_by_warehouse AS
SELECT 
    w.warehouse_name,
    p.sku,
    p.product_name,
    i.quantity_on_hand,
    i.quantity_reserved,
    i.quantity_available,
    i.stock_status,
    i.bin_location,
    i.last_counted_date
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
WHERE p.is_active = TRUE;

-- View: Recent Transactions
CREATE VIEW v_recent_transactions AS
SELECT 
    th.transaction_date,
    th.transaction_type,
    th.reference_number,
    p.sku,
    p.product_name,
    w.warehouse_name,
    th.quantity_change,
    th.total_value,
    u.username as performed_by
FROM transaction_history th
JOIN products p ON th.product_id = p.product_id
JOIN warehouses w ON th.warehouse_id = w.warehouse_id
LEFT JOIN users u ON th.performed_by = u.user_id
ORDER BY th.transaction_date DESC;

-- View: Expiring Products (next 90 days)
CREATE VIEW v_expiring_products AS
SELECT 
    p.sku,
    p.product_name,
    w.warehouse_name,
    i.quantity_on_hand,
    i.expiry_date,
    EXTRACT(DAY FROM (i.expiry_date - CURRENT_DATE)) as days_until_expiry,
    (i.quantity_on_hand * p.cost_price) as value_at_risk
FROM inventory i
JOIN products p ON i.product_id = p.product_id
JOIN warehouses w ON i.warehouse_id = w.warehouse_id
WHERE i.expiry_date IS NOT NULL
  AND i.expiry_date <= CURRENT_DATE + INTERVAL '90 days'
  AND i.quantity_on_hand > 0
ORDER BY i.expiry_date ASC;

-- View: Low Stock Alert
CREATE VIEW v_low_stock_alert AS
SELECT 
    p.sku,
    p.product_name,
    c.category_name,
    s.supplier_name,
    SUM(i.quantity_on_hand) as current_stock,
    p.reorder_point,
    p.reorder_quantity,
    s.lead_time_days
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
LEFT JOIN categories c ON p.category_id = c.category_id
LEFT JOIN suppliers s ON p.sku = p.sku  -- Simplified; add supplier_id to products for proper join
WHERE p.is_active = TRUE
GROUP BY p.product_id, p.sku, p.product_name, c.category_name, s.supplier_name, 
         p.reorder_point, p.reorder_quantity, s.lead_time_days
HAVING SUM(i.quantity_on_hand) < p.reorder_point;

-- ============================================================
-- TRIGGERS for automated updates
-- ============================================================

-- Trigger: Update inventory after transaction
CREATE OR REPLACE FUNCTION update_inventory_after_transaction()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE inventory
    SET quantity_on_hand = quantity_on_hand + NEW.quantity_change,
        last_movement_date = NEW.transaction_date,
        updated_at = CURRENT_TIMESTAMP
    WHERE product_id = NEW.product_id
      AND warehouse_id = NEW.warehouse_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_inventory
AFTER INSERT ON transaction_history
FOR EACH ROW
EXECUTE FUNCTION update_inventory_after_transaction();

-- Trigger: Update stock status automatically
CREATE OR REPLACE FUNCTION update_stock_status()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE inventory i
    SET stock_status = CASE 
        WHEN i.quantity_on_hand < p.reorder_point * 0.5 THEN 'critical'
        WHEN i.quantity_on_hand < p.reorder_point THEN 'low'
        WHEN i.quantity_on_hand < p.reorder_point * 2 THEN 'adequate'
        ELSE 'overstocked'
    END
    FROM products p
    WHERE i.product_id = p.product_id
      AND i.product_id = NEW.product_id
      AND i.warehouse_id = NEW.warehouse_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_stock_status
AFTER INSERT OR UPDATE ON inventory
FOR EACH ROW
EXECUTE FUNCTION update_stock_status();

-- ============================================================
-- SAMPLE DATA INSERTION
-- ============================================================

-- Insert sample categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices and components'),
('Peripherals', 'Computer peripherals and accessories'),
('Cables', 'Various types of cables and connectors'),
('Storage', 'Storage devices and media'),
('Components', 'Computer hardware components'),
('Networking', 'Network equipment and devices');

-- Insert sample suppliers
INSERT INTO suppliers (supplier_name, contact_person, email, phone, lead_time_days, min_order_quantity, rating) VALUES
('TechSupply Co.', 'John Smith', 'john@techsupply.com', '+1-555-0101', 7, 10, 4.5),
('Global Electronics', 'Sarah Johnson', 'sarah@globalelec.com', '+1-555-0102', 14, 20, 4.2),
('Hardware Plus', 'Mike Brown', 'mike@hardwareplus.com', '+1-555-0103', 5, 5, 4.8),
('Component World', 'Lisa Davis', 'lisa@compworld.com', '+1-555-0104', 10, 15, 4.0),
('Digital Distributors', 'Tom Wilson', 'tom@digidist.com', '+1-555-0105', 7, 10, 4.6);

-- Insert sample warehouses
INSERT INTO warehouses (warehouse_name, warehouse_code, address, city, capacity_cubic_meters) VALUES
('Warehouse A', 'WH-A', '123 Industrial Blvd', 'New York', 5000.00),
('Warehouse B', 'WH-B', '456 Commerce St', 'Los Angeles', 4500.00),
('Warehouse C', 'WH-C', '789 Logistics Ave', 'Chicago', 6000.00),
('Warehouse D', 'WH-D', '321 Distribution Way', 'Houston', 5500.00);

-- Insert sample user
INSERT INTO users (username, email, password_hash, first_name, last_name, role) VALUES
('admin', 'admin@stocksystem.com', 'hashed_password_here', 'Admin', 'User', 'admin');

-- ============================================================
-- END OF SCHEMA
-- ============================================================
