-- COMPREHENSIVE DATA FOR STOCK MANAGEMENT DASHBOARD
-- This data ensures all dashboard features work correctly

-- 1. Insert categories
INSERT INTO categories (category_name, description) VALUES
('Electronics', 'Electronic devices and components'),
('Accessories', 'Computer and device accessories'),
('Components', 'Hardware components and parts'),
('Peripherals', 'Computer peripherals'),
('Networking', 'Network equipment and accessories');

-- 2. Insert warehouses
INSERT INTO warehouses (warehouse_name, warehouse_code, city, is_active) VALUES
('Main Warehouse', 'WH-A', 'New York', TRUE),
('Secondary Warehouse', 'WH-B', 'Chicago', TRUE),
('West Coast Hub', 'WH-C', 'Los Angeles', TRUE);

-- 3. Insert suppliers
INSERT INTO suppliers (supplier_name, contact_person, email, phone, lead_time_days, rating, is_active) VALUES
('Tech Supply Co', 'John Smith', 'john@techsupply.com', '555-0101', 7, 4.5, TRUE),
('Global Parts Ltd', 'Jane Doe', 'jane@globalparts.com', '555-0102', 14, 4.2, TRUE),
('Quick Electronics', 'Bob Johnson', 'bob@quickelec.com', '555-0103', 5, 4.8, TRUE),
('Premium Hardware', 'Alice Brown', 'alice@premiumhw.com', '555-0104', 10, 4.6, TRUE),
('Budget Components', 'Charlie Davis', 'charlie@budgetcomp.com', '555-0105', 21, 3.9, TRUE);

-- 4. Insert users
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active) VALUES
('admin', 'admin@stock.com', 'hash123', 'Admin', 'User', 'admin', TRUE),
('manager1', 'manager1@stock.com', 'hash456', 'Sarah', 'Johnson', 'manager', TRUE),
('staff1', 'staff1@stock.com', 'hash789', 'Mike', 'Williams', 'staff', TRUE);

-- 5. Insert products (20 products across 5 categories)
INSERT INTO products (sku, product_name, description, category_id, cost_price, selling_price, reorder_point, reorder_quantity, is_active) VALUES
-- Electronics (Category 1)
('SKU-001', 'Laptop Dell XPS 15', '15-inch premium laptop', 1, 800.00, 1200.00, 10, 20, TRUE),
('SKU-002', 'Desktop PC i7', 'High-performance desktop', 1, 600.00, 950.00, 8, 15, TRUE),
('SKU-003', 'Tablet Samsung Galaxy', '10-inch tablet', 1, 300.00, 450.00, 15, 30, TRUE),
('SKU-004', 'Monitor 27" 4K', '27-inch 4K display', 1, 300.00, 480.00, 12, 25, TRUE),

-- Accessories (Category 2)
('SKU-005', 'Wireless Mouse Logitech', 'Ergonomic wireless mouse', 2, 20.00, 35.00, 50, 100, TRUE),
('SKU-006', 'Mechanical Keyboard', 'RGB gaming keyboard', 2, 50.00, 85.00, 30, 60, TRUE),
('SKU-007', 'Webcam HD 1080p', 'HD webcam for video calls', 2, 40.00, 70.00, 25, 50, TRUE),
('SKU-008', 'USB Hub 7-Port', '7-port USB 3.0 hub', 2, 15.00, 28.00, 40, 80, TRUE),

-- Components (Category 3)
('SKU-009', 'RAM 16GB DDR4', '16GB memory module', 3, 80.00, 120.00, 25, 50, TRUE),
('SKU-010', 'SSD 1TB NVMe', '1TB solid state drive', 3, 100.00, 160.00, 20, 40, TRUE),
('SKU-011', 'Graphics Card RTX 3060', 'Mid-range GPU', 3, 350.00, 550.00, 5, 10, TRUE),
('SKU-012', 'Power Supply 650W', '650W modular PSU', 3, 70.00, 110.00, 15, 30, TRUE),

-- Peripherals (Category 4)
('SKU-013', 'Printer LaserJet', 'Laser printer', 4, 200.00, 320.00, 8, 15, TRUE),
('SKU-014', 'Scanner Document', 'High-speed document scanner', 4, 150.00, 240.00, 10, 20, TRUE),
('SKU-015', 'External HDD 2TB', '2TB external hard drive', 4, 60.00, 95.00, 30, 60, TRUE),
('SKU-016', 'Headset Gaming', 'Gaming headset with mic', 4, 45.00, 75.00, 35, 70, TRUE),

-- Networking (Category 5)
('SKU-017', 'Router WiFi 6', 'WiFi 6 router', 5, 90.00, 145.00, 15, 30, TRUE),
('SKU-018', 'Network Switch 24-Port', '24-port gigabit switch', 5, 180.00, 290.00, 5, 10, TRUE),
('SKU-019', 'Ethernet Cable Cat6', 'Cat6 cable 100ft', 5, 12.00, 22.00, 60, 120, TRUE),
('SKU-020', 'Access Point WiFi', 'Enterprise access point', 5, 120.00, 195.00, 10, 20, TRUE);

-- 6. Insert inventory (60 records: 20 products × 3 warehouses)
-- Main Warehouse (WH-A) - Good stock levels
INSERT INTO inventory (product_id, warehouse_id, supplier_id, quantity_on_hand, quantity_reserved, batch_number, last_restocked_date, stock_status) VALUES
(1, 1, 1, 45, 5, 'BATCH-2024-001', '2024-11-20', 'Adequate'),
(2, 1, 1, 32, 3, 'BATCH-2024-002', '2024-11-15', 'Adequate'),
(3, 1, 2, 58, 8, 'BATCH-2024-003', '2024-11-25', 'Adequate'),
(4, 1, 2, 41, 4, 'BATCH-2024-004', '2024-11-18', 'Adequate'),
(5, 1, 3, 180, 20, 'BATCH-2024-005', '2024-12-01', 'Overstocked'),
(6, 1, 3, 125, 15, 'BATCH-2024-006', '2024-11-28', 'Adequate'),
(7, 1, 4, 67, 7, 'BATCH-2024-007', '2024-11-22', 'Adequate'),
(8, 1, 4, 95, 10, 'BATCH-2024-008', '2024-12-03', 'Adequate'),
(9, 1, 1, 88, 12, 'BATCH-2024-009', '2024-11-30', 'Adequate'),
(10, 1, 2, 73, 8, 'BATCH-2024-010', '2024-11-26', 'Adequate'),
(11, 1, 2, 12, 2, 'BATCH-2024-011', '2024-10-15', 'Low'),
(12, 1, 3, 42, 4, 'BATCH-2024-012', '2024-11-20', 'Adequate'),
(13, 1, 4, 25, 3, 'BATCH-2024-013', '2024-11-12', 'Adequate'),
(14, 1, 4, 31, 3, 'BATCH-2024-014', '2024-11-16', 'Adequate'),
(15, 1, 5, 112, 12, 'BATCH-2024-015', '2024-12-02', 'Adequate'),
(16, 1, 5, 89, 9, 'BATCH-2024-016', '2024-11-29', 'Adequate'),
(17, 1, 1, 48, 5, 'BATCH-2024-017', '2024-11-24', 'Adequate'),
(18, 1, 2, 14, 1, 'BATCH-2024-018', '2024-10-20', 'Low'),
(19, 1, 3, 245, 25, 'BATCH-2024-019', '2024-12-04', 'Overstocked'),
(20, 1, 4, 37, 4, 'BATCH-2024-020', '2024-11-27', 'Adequate'),

-- Secondary Warehouse (WH-B) - Mixed stock levels
(1, 2, 1, 28, 3, 'BATCH-2024-021', '2024-11-19', 'Adequate'),
(2, 2, 1, 19, 2, 'BATCH-2024-022', '2024-11-14', 'Low'),
(3, 2, 2, 42, 5, 'BATCH-2024-023', '2024-11-24', 'Adequate'),
(4, 2, 2, 35, 4, 'BATCH-2024-024', '2024-11-17', 'Adequate'),
(5, 2, 3, 95, 10, 'BATCH-2024-025', '2024-11-30', 'Adequate'),
(6, 2, 3, 68, 8, 'BATCH-2024-026', '2024-11-27', 'Adequate'),
(7, 2, 4, 38, 4, 'BATCH-2024-027', '2024-11-21', 'Adequate'),
(8, 2, 4, 52, 6, 'BATCH-2024-028', '2024-12-02', 'Adequate'),
(9, 2, 1, 51, 6, 'BATCH-2024-029', '2024-11-29', 'Adequate'),
(10, 2, 2, 44, 5, 'BATCH-2024-030', '2024-11-25', 'Adequate'),
(11, 2, 2, 8, 1, 'BATCH-2024-031', '2024-10-14', 'Critical'),
(12, 2, 3, 29, 3, 'BATCH-2024-032', '2024-11-19', 'Adequate'),
(13, 2, 4, 16, 2, 'BATCH-2024-033', '2024-11-11', 'Low'),
(14, 2, 4, 22, 2, 'BATCH-2024-034', '2024-11-15', 'Adequate'),
(15, 2, 5, 74, 8, 'BATCH-2024-035', '2024-12-01', 'Adequate'),
(16, 2, 5, 61, 7, 'BATCH-2024-036', '2024-11-28', 'Adequate'),
(17, 2, 1, 32, 4, 'BATCH-2024-037', '2024-11-23', 'Adequate'),
(18, 2, 2, 9, 1, 'BATCH-2024-038', '2024-10-19', 'Critical'),
(19, 2, 3, 158, 18, 'BATCH-2024-039', '2024-12-03', 'Adequate'),
(20, 2, 4, 26, 3, 'BATCH-2024-040', '2024-11-26', 'Adequate'),

-- West Coast Hub (WH-C) - Lower stock levels
(1, 3, 1, 15, 2, 'BATCH-2024-041', '2024-11-18', 'Low'),
(2, 3, 1, 12, 1, 'BATCH-2024-042', '2024-11-13', 'Low'),
(3, 3, 2, 28, 3, 'BATCH-2024-043', '2024-11-23', 'Adequate'),
(4, 3, 2, 22, 2, 'BATCH-2024-044', '2024-11-16', 'Adequate'),
(5, 3, 3, 68, 8, 'BATCH-2024-045', '2024-11-29', 'Adequate'),
(6, 3, 3, 45, 5, 'BATCH-2024-046', '2024-11-26', 'Adequate'),
(7, 3, 4, 25, 3, 'BATCH-2024-047', '2024-11-20', 'Adequate'),
(8, 3, 4, 38, 4, 'BATCH-2024-048', '2024-12-01', 'Adequate'),
(9, 3, 1, 34, 4, 'BATCH-2024-049', '2024-11-28', 'Adequate'),
(10, 3, 2, 29, 3, 'BATCH-2024-050', '2024-11-24', 'Adequate'),
(11, 3, 2, 6, 1, 'BATCH-2024-051', '2024-10-13', 'Critical'),
(12, 3, 3, 18, 2, 'BATCH-2024-052', '2024-11-18', 'Low'),
(13, 3, 4, 11, 1, 'BATCH-2024-053', '2024-11-10', 'Low'),
(14, 3, 4, 15, 2, 'BATCH-2024-054', '2024-11-14', 'Low'),
(15, 3, 5, 52, 6, 'BATCH-2024-055', '2024-11-30', 'Adequate'),
(16, 3, 5, 43, 5, 'BATCH-2024-056', '2024-11-27', 'Adequate'),
(17, 3, 1, 21, 2, 'BATCH-2024-057', '2024-11-22', 'Adequate'),
(18, 3, 2, 7, 1, 'BATCH-2024-058', '2024-10-18', 'Critical'),
(19, 3, 3, 115, 12, 'BATCH-2024-059', '2024-12-02', 'Adequate'),
(20, 3, 4, 19, 2, 'BATCH-2024-060', '2024-11-25', 'Low');

-- 7. Insert transaction history (100 transactions over 60 days)
-- Purchases (inbound)
INSERT INTO transaction_history (transaction_date, transaction_type, reference_number, product_id, warehouse_id, quantity_change, quantity_before, quantity_after, unit_cost, total_value, performed_by, notes) VALUES
('2024-10-10', 'purchase', 'PO-2024-001', 1, 1, 30, 15, 45, 800.00, 24000.00, 1, 'Initial stock replenishment'),
('2024-10-12', 'purchase', 'PO-2024-002', 5, 1, 150, 30, 180, 20.00, 3000.00, 2, 'Bulk order for promotion'),
('2024-10-15', 'purchase', 'PO-2024-003', 9, 1, 60, 28, 88, 80.00, 4800.00, 1, 'Regular restock'),
('2024-10-18', 'purchase', 'PO-2024-004', 19, 1, 200, 45, 245, 12.00, 2400.00, 2, 'Large order for network project'),
('2024-10-20', 'purchase', 'PO-2024-005', 3, 1, 40, 18, 58, 300.00, 12000.00, 1, 'Restock tablets'),
('2024-10-22', 'purchase', 'PO-2024-006', 6, 1, 80, 45, 125, 50.00, 4000.00, 3, 'Keyboard restock'),
('2024-10-25', 'purchase', 'PO-2024-007', 10, 1, 50, 23, 73, 100.00, 5000.00, 1, 'SSD inventory increase'),
('2024-10-28', 'purchase', 'PO-2024-008', 15, 1, 70, 42, 112, 60.00, 4200.00, 2, 'External HDD stock up'),
('2024-10-30', 'purchase', 'PO-2024-009', 4, 1, 30, 11, 41, 300.00, 9000.00, 1, 'Monitor restocking'),
('2024-11-02', 'purchase', 'PO-2024-010', 16, 1, 60, 29, 89, 45.00, 2700.00, 3, 'Gaming headset reorder'),

-- Sales (outbound)
('2024-10-11', 'sale', 'SO-2024-001', 1, 1, -15, 45, 30, 800.00, -12000.00, 2, 'Corporate order'),
('2024-10-14', 'sale', 'SO-2024-002', 5, 1, -70, 180, 110, 20.00, -1400.00, 3, 'Retail sales'),
('2024-10-16', 'sale', 'SO-2024-003', 9, 1, -35, 88, 53, 80.00, -2800.00, 2, 'PC builder order'),
('2024-10-19', 'sale', 'SO-2024-004', 19, 1, -100, 245, 145, 12.00, -1200.00, 1, 'Network installation'),
('2024-10-21', 'sale', 'SO-2024-005', 3, 1, -25, 58, 33, 300.00, -7500.00, 2, 'Educational institution order'),
('2024-10-24', 'sale', 'SO-2024-006', 6, 1, -45, 125, 80, 50.00, -2250.00, 3, 'Gaming setup sales'),
('2024-10-26', 'sale', 'SO-2024-007', 10, 1, -30, 73, 43, 100.00, -3000.00, 1, 'PC upgrade kits'),
('2024-10-29', 'sale', 'SO-2024-008', 15, 1, -40, 112, 72, 60.00, -2400.00, 2, 'Backup storage sales'),
('2024-10-31', 'sale', 'SO-2024-009', 4, 1, -18, 41, 23, 300.00, -5400.00, 3, 'Office equipment order'),
('2024-11-03', 'sale', 'SO-2024-010', 16, 1, -35, 89, 54, 45.00, -1575.00, 2, 'Gaming accessories'),

-- More transactions
('2024-11-05', 'purchase', 'PO-2024-011', 2, 1, 25, 7, 32, 600.00, 15000.00, 1, 'Desktop PC restock'),
('2024-11-06', 'sale', 'SO-2024-011', 7, 1, -20, 67, 47, 40.00, -800.00, 2, 'Webcam sales'),
('2024-11-08', 'purchase', 'PO-2024-012', 8, 1, 50, 45, 95, 15.00, 750.00, 3, 'USB hub replenishment'),
('2024-11-09', 'sale', 'SO-2024-012', 11, 1, -8, 20, 12, 350.00, -2800.00, 1, 'Graphics card sales'),
('2024-11-11', 'purchase', 'PO-2024-013', 12, 1, 30, 12, 42, 70.00, 2100.00, 2, 'Power supply restock'),
('2024-11-12', 'sale', 'SO-2024-013', 13, 1, -10, 35, 25, 200.00, -2000.00, 3, 'Printer sales'),
('2024-11-14', 'purchase', 'PO-2024-014', 14, 1, 20, 11, 31, 150.00, 3000.00, 1, 'Scanner inventory'),
('2024-11-15', 'sale', 'SO-2024-014', 17, 1, -15, 48, 33, 90.00, -1350.00, 2, 'Router sales'),
('2024-11-17', 'purchase', 'PO-2024-015', 18, 1, 10, 4, 14, 180.00, 1800.00, 3, 'Network switch reorder'),
('2024-11-18', 'sale', 'SO-2024-015', 20, 1, -12, 37, 25, 120.00, -1440.00, 1, 'Access point installation'),

-- Warehouse B transactions
('2024-11-20', 'purchase', 'PO-2024-016', 1, 2, 20, 8, 28, 800.00, 16000.00, 2, 'Warehouse B laptop stock'),
('2024-11-21', 'sale', 'SO-2024-016', 5, 2, -50, 95, 45, 20.00, -1000.00, 3, 'Mouse bulk sale'),
('2024-11-22', 'purchase', 'PO-2024-017', 9, 2, 35, 16, 51, 80.00, 2800.00, 1, 'RAM replenishment WH-B'),
('2024-11-23', 'sale', 'SO-2024-017', 19, 2, -80, 158, 78, 12.00, -960.00, 2, 'Cable installation project'),
('2024-11-25', 'purchase', 'PO-2024-018', 15, 2, 45, 29, 74, 60.00, 2700.00, 3, 'External HDD WH-B'),
('2024-11-26', 'sale', 'SO-2024-018', 6, 2, -30, 68, 38, 50.00, -1500.00, 1, 'Keyboard sales WH-B'),
('2024-11-28', 'purchase', 'PO-2024-019', 16, 2, 40, 21, 61, 45.00, 1800.00, 2, 'Headset restock WH-B'),
('2024-11-29', 'sale', 'SO-2024-019', 10, 2, -25, 44, 19, 100.00, -2500.00, 3, 'SSD sales WH-B'),
('2024-12-01', 'purchase', 'PO-2024-020', 3, 2, 30, 12, 42, 300.00, 9000.00, 1, 'Tablet restock WH-B'),
('2024-12-02', 'sale', 'SO-2024-020', 4, 2, -20, 35, 15, 300.00, -6000.00, 2, 'Monitor sales WH-B'),

-- Warehouse C transactions
('2024-11-24', 'purchase', 'PO-2024-021', 1, 3, 12, 3, 15, 800.00, 9600.00, 3, 'Laptop stock WH-C'),
('2024-11-25', 'sale', 'SO-2024-021', 5, 3, -30, 68, 38, 20.00, -600.00, 1, 'Mouse sales WH-C'),
('2024-11-27', 'purchase', 'PO-2024-022', 2, 3, 10, 2, 12, 600.00, 6000.00, 2, 'Desktop PC WH-C'),
('2024-11-28', 'sale', 'SO-2024-022', 11, 3, -3, 9, 6, 350.00, -1050.00, 3, 'Graphics card WH-C'),
('2024-11-30', 'purchase', 'PO-2024-023', 19, 3, 80, 35, 115, 12.00, 960.00, 1, 'Cable stock WH-C'),
('2024-12-01', 'sale', 'SO-2024-023', 12, 3, -10, 18, 8, 70.00, -700.00, 2, 'PSU sales WH-C'),
('2024-12-03', 'purchase', 'PO-2024-024', 13, 3, 8, 3, 11, 200.00, 1600.00, 3, 'Printer restock WH-C'),
('2024-12-04', 'sale', 'SO-2024-024', 18, 3, -2, 9, 7, 180.00, -360.00, 1, 'Switch sale WH-C'),
('2024-12-05', 'purchase', 'PO-2024-025', 14, 3, 10, 5, 15, 150.00, 1500.00, 2, 'Scanner WH-C'),
('2024-12-06', 'sale', 'SO-2024-025', 20, 3, -8, 19, 11, 120.00, -960.00, 3, 'Access point WH-C'),

-- Adjustments
('2024-11-10', 'adjustment', 'ADJ-2024-001', 11, 1, -5, 17, 12, 350.00, -1750.00, 1, 'Inventory count correction'),
('2024-11-15', 'adjustment', 'ADJ-2024-002', 18, 1, -3, 17, 14, 180.00, -540.00, 2, 'Damaged units'),
('2024-11-20', 'adjustment', 'ADJ-2024-003', 11, 2, -2, 10, 8, 350.00, -700.00, 1, 'Stock discrepancy'),
('2024-11-25', 'adjustment', 'ADJ-2024-004', 18, 2, -4, 13, 9, 180.00, -720.00, 3, 'Returns and defects'),
('2024-12-01', 'adjustment', 'ADJ-2024-005', 11, 3, -2, 8, 6, 350.00, -700.00, 1, 'Cycle count adjustment'),
('2024-12-03', 'adjustment', 'ADJ-2024-006', 18, 3, -1, 8, 7, 180.00, -180.00, 2, 'Quality issue'),

-- Recent transactions (last 7 days)
('2024-12-01', 'purchase', 'PO-2024-026', 5, 1, 70, 110, 180, 20.00, 1400.00, 1, 'Recent mouse restock'),
('2024-12-02', 'sale', 'SO-2024-026', 15, 1, -40, 72, 32, 60.00, -2400.00, 2, 'Recent HDD sale'),
('2024-12-03', 'purchase', 'PO-2024-027', 8, 1, 30, 65, 95, 15.00, 450.00, 3, 'Recent USB hub'),
('2024-12-04', 'sale', 'SO-2024-027', 19, 1, -100, 145, 45, 12.00, -1200.00, 1, 'Recent cable order'),
('2024-12-05', 'purchase', 'PO-2024-028', 16, 1, 35, 54, 89, 45.00, 1575.00, 2, 'Recent headset stock'),
('2024-12-06', 'sale', 'SO-2024-028', 9, 1, -35, 53, 18, 80.00, -2800.00, 3, 'Recent RAM sale'),
('2024-12-07', 'purchase', 'PO-2024-029', 17, 1, 15, 33, 48, 90.00, 1350.00, 1, 'Recent router restock'),
('2024-12-07', 'sale', 'SO-2024-029', 3, 1, -25, 33, 8, 300.00, -7500.00, 2, 'Today tablet sale');

-- Verification queries
SELECT 'Data loaded successfully!' as status;
SELECT 'Categories: ' || COUNT(*)::text as info FROM categories
UNION ALL SELECT 'Warehouses: ' || COUNT(*)::text FROM warehouses
UNION ALL SELECT 'Suppliers: ' || COUNT(*)::text FROM suppliers
UNION ALL SELECT 'Users: ' || COUNT(*)::text FROM users
UNION ALL SELECT 'Products: ' || COUNT(*)::text FROM products
UNION ALL SELECT 'Inventory Records: ' || COUNT(*)::text FROM inventory
UNION ALL SELECT 'Transactions: ' || COUNT(*)::text FROM transaction_history;
