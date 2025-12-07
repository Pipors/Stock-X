-- ============================================================
-- SAMPLE DATA POPULATION SCRIPT
-- Populates the stock management database with realistic test data
-- ============================================================

-- ============================================================
-- 1. INSERT USERS
-- ============================================================
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active) VALUES
('admin', 'admin@stocksystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsJQMmjpNtDa', 'Admin', 'User', 'admin', TRUE),
('john.manager', 'john.manager@stocksystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsJQMmjpNtDa', 'John', 'Manager', 'manager', TRUE),
('sarah.staff', 'sarah.staff@stocksystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsJQMmjpNtDa', 'Sarah', 'Johnson', 'warehouse_staff', TRUE),
('mike.staff', 'mike.staff@stocksystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsJQMmjpNtDa', 'Mike', 'Williams', 'warehouse_staff', TRUE),
('viewer', 'viewer@stocksystem.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5lsJQMmjpNtDa', 'View', 'Only', 'viewer', TRUE);

-- ============================================================
-- 2. INSERT CATEGORIES
-- ============================================================
INSERT INTO categories (category_name, description, parent_category_id) VALUES
('Electronics', 'Electronic devices and equipment', NULL),
('Peripherals', 'Computer peripheral devices', NULL),
('Cables & Connectors', 'Various cables and connectors', NULL),
('Storage Devices', 'Data storage hardware', NULL),
('Computer Components', 'Internal computer parts', NULL),
('Networking Equipment', 'Network devices and accessories', NULL);

-- ============================================================
-- 3. INSERT SUPPLIERS
-- ============================================================
INSERT INTO suppliers (supplier_name, contact_person, email, phone, address, city, country, postal_code, payment_terms, lead_time_days, min_order_quantity, is_active, rating) VALUES
('TechSupply Co.', 'John Smith', 'john.smith@techsupply.com', '+1-555-0101', '123 Tech Avenue', 'New York', 'USA', '10001', 'Net 30', 7, 10, TRUE, 4.5),
('Global Electronics', 'Sarah Johnson', 'sarah.j@globalelec.com', '+1-555-0102', '456 Commerce Blvd', 'Los Angeles', 'USA', '90001', 'Net 45', 14, 20, TRUE, 4.2),
('Hardware Plus', 'Mike Brown', 'mike.b@hardwareplus.com', '+1-555-0103', '789 Industrial Way', 'Chicago', 'USA', '60601', 'Net 30', 5, 5, TRUE, 4.8),
('Component World', 'Lisa Davis', 'lisa.d@compworld.com', '+1-555-0104', '321 Tech Park', 'Austin', 'USA', '73301', 'Net 60', 10, 15, TRUE, 4.0),
('Digital Distributors', 'Tom Wilson', 'tom.w@digidist.com', '+1-555-0105', '654 Supply Street', 'Seattle', 'USA', '98101', 'Net 30', 7, 10, TRUE, 4.6),
('Prime Components', 'Emily Chen', 'emily.c@primecomp.com', '+1-555-0106', '987 Component Lane', 'San Francisco', 'USA', '94101', 'Net 45', 12, 25, TRUE, 4.3),
('Reliable Tech', 'David Martinez', 'david.m@reliabletech.com', '+1-555-0107', '147 Vendor Road', 'Boston', 'USA', '02101', 'Net 30', 6, 10, TRUE, 4.7);

-- ============================================================
-- 4. INSERT WAREHOUSES
-- ============================================================
INSERT INTO warehouses (warehouse_name, warehouse_code, address, city, country, postal_code, capacity_cubic_meters, manager_name, phone, is_active) VALUES
('Warehouse A - East Coast', 'WH-A', '123 Industrial Blvd', 'New York', 'USA', '10001', 5000.00, 'Robert Johnson', '+1-555-1001', TRUE),
('Warehouse B - West Coast', 'WH-B', '456 Commerce St', 'Los Angeles', 'USA', '90001', 4500.00, 'Maria Garcia', '+1-555-1002', TRUE),
('Warehouse C - Central', 'WH-C', '789 Logistics Ave', 'Chicago', 'USA', '60601', 6000.00, 'James Wilson', '+1-555-1003', TRUE),
('Warehouse D - South', 'WH-D', '321 Distribution Way', 'Houston', 'USA', '77001', 5500.00, 'Patricia Brown', '+1-555-1004', TRUE);

-- ============================================================
-- 5. INSERT PRODUCTS (20 products matching mock data)
-- ============================================================
INSERT INTO products (sku, product_name, description, category_id, brand, cost_price, selling_price, reorder_point, reorder_quantity, min_stock_level, max_stock_level, weight_kg, unit_of_measure, has_expiry, abc_classification, velocity_classification, is_active) VALUES
-- Electronics
('SKU-1000', 'Laptop', 'High-performance business laptop', 1, 'Dell', 650.00, 999.99, 20, 50, 10, 200, 2.5, 'pieces', FALSE, 'A', 'fast', TRUE),
('SKU-1009', 'Printer', 'Multi-function laser printer', 1, 'HP', 280.00, 449.99, 15, 30, 5, 100, 8.5, 'pieces', FALSE, 'B', 'medium', TRUE),
('SKU-1010', 'Scanner', 'Document scanner with OCR', 1, 'Canon', 180.00, 299.99, 10, 25, 5, 80, 3.2, 'pieces', FALSE, 'C', 'slow', TRUE),

-- Peripherals
('SKU-1001', 'Mouse', 'Wireless optical mouse', 2, 'Logitech', 15.00, 29.99, 50, 100, 20, 500, 0.1, 'pieces', FALSE, 'B', 'fast', TRUE),
('SKU-1002', 'Keyboard', 'Mechanical gaming keyboard', 2, 'Razer', 75.00, 129.99, 30, 60, 15, 300, 1.2, 'pieces', FALSE, 'A', 'fast', TRUE),
('SKU-1003', 'Monitor', '27-inch 4K display', 2, 'Samsung', 320.00, 549.99, 25, 40, 10, 150, 6.8, 'pieces', FALSE, 'A', 'medium', TRUE),
('SKU-1006', 'Webcam', '1080p HD webcam with microphone', 2, 'Logitech', 45.00, 79.99, 40, 80, 15, 250, 0.3, 'pieces', FALSE, 'B', 'fast', TRUE),
('SKU-1007', 'Headphones', 'Noise-cancelling wireless headphones', 2, 'Sony', 120.00, 199.99, 35, 70, 15, 200, 0.4, 'pieces', FALSE, 'A', 'fast', TRUE),

-- Cables & Connectors
('SKU-1004', 'USB Cable', 'USB-C to USB-A cable 6ft', 3, 'Anker', 5.00, 12.99, 100, 200, 50, 1000, 0.05, 'pieces', FALSE, 'C', 'fast', TRUE),
('SKU-1005', 'HDMI Cable', 'HDMI 2.1 cable 10ft', 3, 'AmazonBasics', 8.00, 19.99, 80, 150, 40, 800, 0.15, 'pieces', FALSE, 'C', 'fast', TRUE),

-- Networking Equipment
('SKU-1011', 'Router', 'Dual-band WiFi 6 router', 6, 'TP-Link', 85.00, 149.99, 20, 40, 10, 120, 0.8, 'pieces', FALSE, 'B', 'medium', TRUE),
('SKU-1012', 'Switch', '8-port gigabit network switch', 6, 'Netgear', 45.00, 89.99, 25, 50, 10, 150, 0.6, 'pieces', FALSE, 'C', 'medium', TRUE),

-- Storage Devices
('SKU-1013', 'Hard Drive', '2TB external HDD', 4, 'Western Digital', 60.00, 99.99, 40, 80, 20, 300, 0.2, 'pieces', FALSE, 'B', 'fast', TRUE),
('SKU-1014', 'SSD', '1TB NVMe SSD', 4, 'Samsung', 95.00, 159.99, 35, 70, 15, 250, 0.01, 'pieces', FALSE, 'A', 'fast', TRUE),

-- Computer Components
('SKU-1015', 'RAM Module', '16GB DDR4 RAM', 5, 'Corsair', 55.00, 89.99, 50, 100, 25, 400, 0.05, 'pieces', FALSE, 'B', 'fast', TRUE),
('SKU-1016', 'Graphics Card', 'RTX 3060 GPU', 5, 'NVIDIA', 420.00, 699.99, 15, 30, 5, 100, 1.2, 'pieces', FALSE, 'A', 'medium', TRUE),
('SKU-1017', 'Motherboard', 'ATX gaming motherboard', 5, 'ASUS', 180.00, 299.99, 20, 40, 10, 120, 1.5, 'pieces', FALSE, 'B', 'slow', TRUE),
('SKU-1018', 'Power Supply', '750W modular PSU', 5, 'EVGA', 95.00, 159.99, 30, 60, 15, 200, 2.0, 'pieces', FALSE, 'C', 'medium', TRUE),
('SKU-1019', 'CPU', 'Intel Core i7 processor', 5, 'Intel', 320.00, 529.99, 18, 35, 8, 100, 0.1, 'pieces', FALSE, 'A', 'medium', TRUE),
('SKU-1020', 'Cooling Fan', 'RGB CPU cooler', 5, 'Cooler Master', 35.00, 69.99, 45, 90, 20, 300, 0.7, 'pieces', FALSE, 'C', 'medium', TRUE);

-- ============================================================
-- 6. INSERT INVENTORY (Stock for each product in warehouses)
-- ============================================================
INSERT INTO inventory (product_id, warehouse_id, quantity_on_hand, quantity_reserved, aisle, rack, shelf, bin_location, last_counted_date, last_restocked_date, batch_number, stock_status, quality_status) VALUES
-- Warehouse A (WH-A)
(1, 1, 85, 10, 'A', '12', '3', 'A-12-3-01', '2025-12-01', '2025-11-15', 'BATCH-2024-Q4-001', 'adequate', 'approved'),
(2, 1, 320, 25, 'B', '05', '2', 'B-05-2-02', '2025-12-01', '2025-11-20', 'BATCH-2024-Q4-002', 'overstocked', 'approved'),
(3, 1, 165, 15, 'A', '08', '4', 'A-08-4-03', '2025-12-01', '2025-11-10', 'BATCH-2024-Q4-003', 'adequate', 'approved'),
(4, 1, 245, 20, 'B', '03', '1', 'B-03-1-04', '2025-12-01', '2025-11-25', 'BATCH-2024-Q4-004', 'overstocked', 'approved'),
(5, 1, 420, 50, 'C', '15', '3', 'C-15-3-05', '2025-12-01', '2025-11-18', 'BATCH-2024-Q4-005', 'overstocked', 'approved'),
(6, 1, 390, 40, 'C', '12', '2', 'C-12-2-06', '2025-12-01', '2025-11-22', 'BATCH-2024-Q4-006', 'overstocked', 'approved'),
(7, 1, 42, 5, 'A', '18', '4', 'A-18-4-07', '2025-12-01', '2025-10-30', 'BATCH-2024-Q3-007', 'adequate', 'approved'),
(8, 1, 18, 2, 'B', '14', '3', 'B-14-3-08', '2025-12-01', '2025-10-15', 'BATCH-2024-Q3-008', 'critical', 'approved'),
(9, 1, 125, 15, 'A', '22', '2', 'A-22-2-09', '2025-12-01', '2025-11-28', 'BATCH-2024-Q4-009', 'adequate', 'approved'),
(10, 1, 28, 3, 'B', '08', '4', 'B-08-4-10', '2025-12-01', '2025-10-20', 'BATCH-2024-Q3-010', 'low', 'approved'),
(11, 1, 95, 10, 'A', '15', '1', 'A-15-1-11', '2025-12-01', '2025-11-12', 'BATCH-2024-Q4-011', 'adequate', 'approved'),
(12, 1, 180, 20, 'B', '11', '3', 'B-11-3-12', '2025-12-01', '2025-11-05', 'BATCH-2024-Q4-012', 'overstocked', 'approved'),
(13, 1, 215, 25, 'C', '09', '2', 'C-09-2-13', '2025-12-01', '2025-11-19', 'BATCH-2024-Q4-013', 'overstocked', 'approved'),
(14, 1, 168, 18, 'A', '20', '4', 'A-20-4-14', '2025-12-01', '2025-11-23', 'BATCH-2024-Q4-014', 'adequate', 'approved'),
(15, 1, 285, 30, 'B', '16', '1', 'B-16-1-15', '2025-12-01', '2025-11-26', 'BATCH-2024-Q4-015', 'overstocked', 'approved'),
(16, 1, 32, 4, 'A', '25', '3', 'A-25-3-16', '2025-12-01', '2025-10-28', 'BATCH-2024-Q3-016', 'adequate', 'approved'),
(17, 1, 45, 5, 'B', '19', '2', 'B-19-2-17', '2025-12-01', '2025-11-08', 'BATCH-2024-Q4-017', 'adequate', 'approved'),
(18, 1, 125, 15, 'C', '07', '4', 'C-07-4-18', '2025-12-01', '2025-11-15', 'BATCH-2024-Q4-018', 'adequate', 'approved'),
(19, 1, 38, 4, 'A', '28', '1', 'A-28-1-19', '2025-12-01', '2025-10-25', 'BATCH-2024-Q3-019', 'adequate', 'approved'),
(20, 1, 195, 20, 'B', '21', '3', 'B-21-3-20', '2025-12-01', '2025-11-20', 'BATCH-2024-Q4-020', 'overstocked', 'approved'),

-- Warehouse B (WH-B)
(1, 2, 72, 8, 'D', '10', '2', 'D-10-2-01', '2025-12-02', '2025-11-18', 'BATCH-2024-Q4-021', 'adequate', 'approved'),
(2, 2, 145, 12, 'E', '04', '3', 'E-04-3-02', '2025-12-02', '2025-11-22', 'BATCH-2024-Q4-022', 'adequate', 'approved'),
(3, 2, 88, 8, 'D', '07', '1', 'D-07-1-03', '2025-12-02', '2025-11-12', 'BATCH-2024-Q4-023', 'adequate', 'approved'),
(4, 2, 92, 9, 'E', '02', '4', 'E-02-4-04', '2025-12-02', '2025-11-27', 'BATCH-2024-Q4-024', 'adequate', 'approved'),
(5, 2, 185, 18, 'F', '13', '2', 'F-13-2-05', '2025-12-02', '2025-11-20', 'BATCH-2024-Q4-025', 'adequate', 'approved'),
(6, 2, 165, 16, 'F', '11', '3', 'F-11-3-06', '2025-12-02', '2025-11-24', 'BATCH-2024-Q4-026', 'adequate', 'approved'),
(7, 2, 35, 3, 'D', '16', '1', 'D-16-1-07', '2025-12-02', '2025-11-01', 'BATCH-2024-Q4-027', 'adequate', 'approved'),
(8, 2, 8, 1, 'E', '12', '4', 'E-12-4-08', '2025-12-02', '2025-10-18', 'BATCH-2024-Q3-028', 'critical', 'approved'),
(9, 2, 58, 6, 'D', '20', '3', 'D-20-3-09', '2025-12-02', '2025-11-30', 'BATCH-2024-Q4-029', 'adequate', 'approved'),
(10, 2, 15, 2, 'E', '06', '2', 'E-06-2-10', '2025-12-02', '2025-10-22', 'BATCH-2024-Q3-030', 'low', 'approved'),
(11, 2, 42, 4, 'D', '14', '4', 'D-14-4-11', '2025-12-02', '2025-11-14', 'BATCH-2024-Q4-031', 'adequate', 'approved'),
(12, 2, 68, 7, 'E', '09', '1', 'E-09-1-12', '2025-12-02', '2025-11-07', 'BATCH-2024-Q4-032', 'adequate', 'approved'),
(13, 2, 95, 10, 'F', '08', '3', 'F-08-3-13', '2025-12-02', '2025-11-21', 'BATCH-2024-Q4-033', 'adequate', 'approved'),
(14, 2, 78, 8, 'D', '18', '2', 'D-18-2-14', '2025-12-02', '2025-11-25', 'BATCH-2024-Q4-034', 'adequate', 'approved'),
(15, 2, 125, 12, 'E', '15', '4', 'E-15-4-15', '2025-12-02', '2025-11-28', 'BATCH-2024-Q4-035', 'adequate', 'approved'),
(16, 2, 18, 2, 'D', '23', '1', 'D-23-1-16', '2025-12-02', '2025-10-30', 'BATCH-2024-Q3-036', 'low', 'approved'),
(17, 2, 22, 2, 'E', '17', '3', 'E-17-3-17', '2025-12-02', '2025-11-10', 'BATCH-2024-Q4-037', 'adequate', 'approved'),
(18, 2, 55, 6, 'F', '05', '2', 'F-05-2-18', '2025-12-02', '2025-11-17', 'BATCH-2024-Q4-038', 'adequate', 'approved'),
(19, 2, 21, 2, 'D', '26', '4', 'D-26-4-19', '2025-12-02', '2025-10-27', 'BATCH-2024-Q3-039', 'adequate', 'approved'),
(20, 2, 88, 9, 'E', '19', '1', 'E-19-1-20', '2025-12-02', '2025-11-22', 'BATCH-2024-Q4-040', 'adequate', 'approved'),

-- Warehouse C (WH-C)
(1, 3, 48, 5, 'G', '11', '3', 'G-11-3-01', '2025-12-03', '2025-11-16', 'BATCH-2024-Q4-041', 'adequate', 'approved'),
(2, 3, 98, 10, 'H', '03', '2', 'H-03-2-02', '2025-12-03', '2025-11-21', 'BATCH-2024-Q4-042', 'adequate', 'approved'),
(3, 3, 55, 5, 'G', '06', '4', 'G-06-4-03', '2025-12-03', '2025-11-11', 'BATCH-2024-Q4-043', 'adequate', 'approved'),
(4, 3, 62, 6, 'H', '01', '1', 'H-01-1-04', '2025-12-03', '2025-11-26', 'BATCH-2024-Q4-044', 'adequate', 'approved'),
(5, 3, 135, 13, 'I', '14', '3', 'I-14-3-05', '2025-12-03', '2025-11-19', 'BATCH-2024-Q4-045', 'adequate', 'approved'),
(6, 3, 118, 12, 'I', '10', '2', 'I-10-2-06', '2025-12-03', '2025-11-23', 'BATCH-2024-Q4-046', 'adequate', 'approved'),
(7, 3, 25, 2, 'G', '17', '4', 'G-17-4-07', '2025-12-03', '2025-11-02', 'BATCH-2024-Q4-047', 'adequate', 'approved'),
(8, 3, 5, 0, 'H', '13', '1', 'H-13-1-08', '2025-12-03', '2025-10-16', 'BATCH-2024-Q3-048', 'critical', 'approved'),
(9, 3, 42, 4, 'G', '21', '3', 'G-21-3-09', '2025-12-03', '2025-11-29', 'BATCH-2024-Q4-049', 'adequate', 'approved'),
(10, 3, 12, 1, 'H', '05', '2', 'H-05-2-10', '2025-12-03', '2025-10-21', 'BATCH-2024-Q3-050', 'low', 'approved'),
(11, 3, 32, 3, 'G', '13', '4', 'G-13-4-11', '2025-12-03', '2025-11-13', 'BATCH-2024-Q4-051', 'adequate', 'approved'),
(12, 3, 48, 5, 'H', '08', '1', 'H-08-1-12', '2025-12-03', '2025-11-06', 'BATCH-2024-Q4-052', 'adequate', 'approved'),
(13, 3, 68, 7, 'I', '07', '3', 'I-07-3-13', '2025-12-03', '2025-11-20', 'BATCH-2024-Q4-053', 'adequate', 'approved'),
(14, 3, 58, 6, 'G', '19', '2', 'G-19-2-14', '2025-12-03', '2025-11-24', 'BATCH-2024-Q4-054', 'adequate', 'approved'),
(15, 3, 92, 9, 'H', '16', '4', 'H-16-4-15', '2025-12-03', '2025-11-27', 'BATCH-2024-Q4-055', 'adequate', 'approved'),
(16, 3, 12, 1, 'G', '24', '1', 'G-24-1-16', '2025-12-03', '2025-10-29', 'BATCH-2024-Q3-056', 'critical', 'approved'),
(17, 3, 18, 2, 'H', '18', '3', 'H-18-3-17', '2025-12-03', '2025-11-09', 'BATCH-2024-Q4-057', 'low', 'approved'),
(18, 3, 42, 4, 'I', '04', '2', 'I-04-2-18', '2025-12-03', '2025-11-16', 'BATCH-2024-Q4-058', 'adequate', 'approved'),
(19, 3, 16, 2, 'G', '27', '4', 'G-27-4-19', '2025-12-03', '2025-10-26', 'BATCH-2024-Q3-059', 'low', 'approved'),
(20, 3, 65, 6, 'H', '20', '1', 'H-20-1-20', '2025-12-03', '2025-11-21', 'BATCH-2024-Q4-060', 'adequate', 'approved'),

-- Warehouse D (WH-D)
(1, 4, 38, 4, 'J', '09', '2', 'J-09-2-01', '2025-12-04', '2025-11-17', 'BATCH-2024-Q4-061', 'adequate', 'approved'),
(2, 4, 75, 7, 'K', '02', '3', 'K-02-3-02', '2025-12-04', '2025-11-19', 'BATCH-2024-Q4-062', 'adequate', 'approved'),
(3, 4, 42, 4, 'J', '05', '1', 'J-05-1-03', '2025-12-04', '2025-11-13', 'BATCH-2024-Q4-063', 'adequate', 'approved'),
(4, 4, 48, 5, 'K', '04', '4', 'K-04-4-04', '2025-12-04', '2025-11-24', 'BATCH-2024-Q4-064', 'adequate', 'approved'),
(5, 4, 105, 10, 'L', '12', '2', 'L-12-2-05', '2025-12-04', '2025-11-17', 'BATCH-2024-Q4-065', 'adequate', 'approved'),
(6, 4, 95, 9, 'L', '09', '3', 'L-09-3-06', '2025-12-04', '2025-11-21', 'BATCH-2024-Q4-066', 'adequate', 'approved'),
(7, 4, 18, 2, 'J', '15', '1', 'J-15-1-07', '2025-12-04', '2025-10-29', 'BATCH-2024-Q3-067', 'low', 'approved'),
(8, 4, 4, 0, 'K', '11', '4', 'K-11-4-08', '2025-12-04', '2025-10-17', 'BATCH-2024-Q3-068', 'critical', 'approved'),
(9, 4, 32, 3, 'J', '19', '3', 'J-19-3-09', '2025-12-04', '2025-11-27', 'BATCH-2024-Q4-069', 'adequate', 'approved'),
(10, 4, 9, 1, 'K', '07', '2', 'K-07-2-10', '2025-12-04', '2025-10-19', 'BATCH-2024-Q3-070', 'critical', 'approved'),
(11, 4, 25, 2, 'J', '12', '4', 'J-12-4-11', '2025-12-04', '2025-11-11', 'BATCH-2024-Q4-071', 'adequate', 'approved'),
(12, 4, 38, 4, 'K', '10', '1', 'K-10-1-12', '2025-12-04', '2025-11-04', 'BATCH-2024-Q4-072', 'adequate', 'approved'),
(13, 4, 52, 5, 'L', '06', '3', 'L-06-3-13', '2025-12-04', '2025-11-18', 'BATCH-2024-Q4-073', 'adequate', 'approved'),
(14, 4, 45, 4, 'J', '17', '2', 'J-17-2-14', '2025-12-04', '2025-11-22', 'BATCH-2024-Q4-074', 'adequate', 'approved'),
(15, 4, 72, 7, 'K', '14', '4', 'K-14-4-15', '2025-12-04', '2025-11-25', 'BATCH-2024-Q4-075', 'adequate', 'approved'),
(16, 4, 10, 1, 'J', '22', '1', 'J-22-1-16', '2025-12-04', '2025-10-31', 'BATCH-2024-Q3-076', 'critical', 'approved'),
(17, 4, 14, 1, 'K', '16', '3', 'K-16-3-17', '2025-12-04', '2025-11-07', 'BATCH-2024-Q4-077', 'critical', 'approved'),
(18, 4, 35, 3, 'L', '03', '2', 'L-03-2-18', '2025-12-04', '2025-11-14', 'BATCH-2024-Q4-078', 'adequate', 'approved'),
(19, 4, 13, 1, 'J', '25', '4', 'J-25-4-19', '2025-12-04', '2025-10-24', 'BATCH-2024-Q3-079', 'critical', 'approved'),
(20, 4, 52, 5, 'K', '18', '1', 'K-18-1-20', '2025-12-04', '2025-11-19', 'BATCH-2024-Q4-080', 'adequate', 'approved');

-- ============================================================
-- 7. INSERT PURCHASE ORDERS
-- ============================================================
INSERT INTO purchase_orders (po_number, supplier_id, warehouse_id, order_date, expected_delivery_date, actual_delivery_date, status, total_amount, tax_amount, shipping_cost, created_by, approved_by, received_by, notes) VALUES
('PO-2024-001', 1, 1, '2024-11-01', '2024-11-08', '2024-11-07', 'received', 32500.00, 2600.00, 150.00, 2, 1, 3, 'Bulk order for laptops and monitors'),
('PO-2024-002', 2, 2, '2024-11-05', '2024-11-19', '2024-11-18', 'received', 15800.00, 1264.00, 200.00, 2, 1, 4, 'Peripheral devices restock'),
('PO-2024-003', 3, 1, '2024-11-10', '2024-11-15', '2024-11-14', 'received', 8500.00, 680.00, 75.00, 2, 1, 3, 'Quick turnaround order'),
('PO-2024-004', 4, 3, '2024-11-12', '2024-11-22', '2024-11-23', 'received', 12300.00, 984.00, 125.00, 2, 1, 3, 'Component restocking'),
('PO-2024-005', 5, 4, '2024-11-15', '2024-11-22', '2024-11-21', 'received', 18900.00, 1512.00, 175.00, 2, 1, 4, 'Storage devices bulk order'),
('PO-2024-006', 1, 2, '2024-11-20', '2024-11-27', NULL, 'ordered', 25600.00, 2048.00, 150.00, 2, 1, NULL, 'Awaiting delivery'),
('PO-2024-007', 6, 1, '2024-11-25', '2024-12-07', NULL, 'ordered', 19400.00, 1552.00, 180.00, 2, 1, NULL, 'Graphics cards and processors'),
('PO-2024-008', 3, 3, '2024-11-28', '2024-12-03', NULL, 'approved', 9200.00, 736.00, 90.00, 2, 1, NULL, 'Cable and connector restock'),
('PO-2024-009', 7, 4, '2024-12-01', '2024-12-07', NULL, 'pending', 14500.00, 1160.00, 140.00, 2, NULL, NULL, 'Awaiting approval'),
('PO-2024-010', 2, 1, '2024-12-03', '2024-12-17', NULL, 'pending', 22100.00, 1768.00, 200.00, 2, NULL, NULL, 'End of year stock up');

-- ============================================================
-- 8. INSERT PURCHASE ORDER ITEMS
-- ============================================================
INSERT INTO purchase_order_items (po_id, product_id, quantity_ordered, quantity_received, unit_price, batch_number, manufacturing_date, expiry_date) VALUES
-- PO-2024-001
(1, 1, 50, 50, 650.00, 'BATCH-2024-Q4-001', '2024-10-15', NULL),
(1, 3, 20, 20, 320.00, 'BATCH-2024-Q4-003', '2024-10-18', NULL),
(1, 16, 10, 10, 420.00, 'BATCH-2024-Q3-016', '2024-09-20', NULL),

-- PO-2024-002
(2, 2, 100, 100, 15.00, 'BATCH-2024-Q4-002', '2024-10-20', NULL),
(2, 6, 50, 50, 45.00, 'BATCH-2024-Q4-006', '2024-10-22', NULL),
(2, 7, 40, 40, 120.00, 'BATCH-2024-Q4-007', '2024-10-25', NULL),

-- PO-2024-003
(3, 4, 200, 200, 5.00, 'BATCH-2024-Q4-005', '2024-10-28', NULL),
(3, 5, 150, 150, 8.00, 'BATCH-2024-Q4-004', '2024-10-30', NULL),
(3, 20, 100, 100, 35.00, 'BATCH-2024-Q4-020', '2024-11-01', NULL),

-- PO-2024-004
(4, 15, 120, 120, 55.00, 'BATCH-2024-Q4-015', '2024-11-05', NULL),
(4, 17, 25, 25, 180.00, 'BATCH-2024-Q4-017', '2024-11-08', NULL),
(4, 18, 40, 40, 95.00, 'BATCH-2024-Q4-018', '2024-11-10', NULL),

-- PO-2024-005
(5, 13, 80, 80, 60.00, 'BATCH-2024-Q4-013', '2024-11-12', NULL),
(5, 14, 70, 70, 95.00, 'BATCH-2024-Q4-014', '2024-11-14', NULL),
(5, 11, 30, 30, 85.00, 'BATCH-2024-Q4-011', '2024-11-16', NULL),

-- PO-2024-006 (Not received yet)
(6, 1, 40, 0, 650.00, 'BATCH-2024-Q4-081', '2024-11-18', NULL),
(6, 19, 20, 0, 320.00, 'BATCH-2024-Q4-082', '2024-11-20', NULL),

-- PO-2024-007 (Not received yet)
(7, 16, 15, 0, 420.00, 'BATCH-2024-Q4-083', '2024-11-22', NULL),
(7, 19, 25, 0, 320.00, 'BATCH-2024-Q4-084', '2024-11-24', NULL),

-- PO-2024-008 (Not received yet)
(8, 4, 300, 0, 5.00, 'BATCH-2024-Q4-085', '2024-11-26', NULL),
(8, 5, 250, 0, 8.00, 'BATCH-2024-Q4-086', '2024-11-28', NULL),

-- PO-2024-009 (Pending)
(9, 9, 50, 0, 280.00, 'BATCH-2024-Q4-087', '2024-11-30', NULL),
(9, 10, 40, 0, 180.00, 'BATCH-2024-Q4-088', '2024-12-01', NULL),

-- PO-2024-010 (Pending)
(10, 2, 200, 0, 15.00, 'BATCH-2024-Q4-089', '2024-12-02', NULL),
(10, 8, 60, 0, 75.00, 'BATCH-2024-Q4-090', '2024-12-03', NULL);

-- ============================================================
-- 9. INSERT SALES ORDERS
-- ============================================================
INSERT INTO sales_orders (so_number, customer_name, customer_email, warehouse_id, order_date, required_date, shipped_date, status, total_amount, tax_amount, shipping_cost, created_by, processed_by, notes) VALUES
('SO-2024-001', 'ABC Corporation', 'orders@abccorp.com', 1, '2024-11-01', '2024-11-05', '2024-11-04', 'delivered', 8500.00, 680.00, 50.00, 2, 3, 'Regular customer - priority shipping'),
('SO-2024-002', 'Tech Solutions Inc', 'purchasing@techsolutions.com', 2, '2024-11-03', '2024-11-08', '2024-11-07', 'delivered', 15600.00, 1248.00, 75.00, 2, 4, 'Bulk order'),
('SO-2024-003', 'Small Business LLC', 'admin@smallbiz.com', 1, '2024-11-05', '2024-11-10', '2024-11-09', 'delivered', 3200.00, 256.00, 25.00, 2, 3, 'First time customer'),
('SO-2024-004', 'Enterprise Systems', 'orders@enterprise.com', 3, '2024-11-08', '2024-11-15', '2024-11-14', 'delivered', 22400.00, 1792.00, 100.00, 2, 3, 'Major client - volume discount applied'),
('SO-2024-005', 'Startup Hub', 'buying@startuphub.com', 4, '2024-11-12', '2024-11-18', '2024-11-17', 'delivered', 9800.00, 784.00, 60.00, 2, 4, 'Office setup order'),
('SO-2024-006', 'Government Agency', 'procurement@gov.org', 1, '2024-11-15', '2024-11-25', '2024-11-24', 'delivered', 34500.00, 2760.00, 150.00, 2, 3, 'Government contract fulfillment'),
('SO-2024-007', 'Retail Chain', 'orders@retailchain.com', 2, '2024-11-20', '2024-11-27', '2024-11-26', 'shipped', 18700.00, 1496.00, 85.00, 2, 4, 'Store restocking'),
('SO-2024-008', 'Educational Institute', 'purchases@university.edu', 3, '2024-11-22', '2024-12-01', NULL, 'processing', 28900.00, 2312.00, 120.00, 2, 3, 'Lab equipment order'),
('SO-2024-009', 'Healthcare Provider', 'it@hospital.org', 4, '2024-11-28', '2024-12-05', NULL, 'processing', 16300.00, 1304.00, 90.00, 2, 4, 'IT department order'),
('SO-2024-010', 'Manufacturing Co', 'supply@manufacturing.com', 1, '2024-12-02', '2024-12-10', NULL, 'pending', 21500.00, 1720.00, 110.00, 2, NULL, 'Large equipment order');

-- ============================================================
-- 10. INSERT SALES ORDER ITEMS
-- ============================================================
INSERT INTO sales_order_items (so_id, product_id, quantity_ordered, quantity_shipped, unit_price) VALUES
-- SO-2024-001
(1, 1, 5, 5, 999.99),
(1, 2, 20, 20, 29.99),
(1, 3, 10, 10, 549.99),

-- SO-2024-002
(2, 8, 25, 25, 129.99),
(2, 13, 30, 30, 99.99),
(2, 14, 40, 40, 159.99),

-- SO-2024-003
(3, 4, 50, 50, 12.99),
(3, 5, 40, 40, 19.99),
(3, 2, 30, 30, 29.99),

-- SO-2024-004
(4, 1, 20, 20, 999.99),
(4, 3, 15, 15, 549.99),
(4, 16, 8, 8, 699.99),

-- SO-2024-005
(5, 2, 50, 50, 29.99),
(5, 3, 8, 8, 549.99),
(5, 11, 12, 12, 149.99),
(5, 13, 20, 20, 99.99),

-- SO-2024-006
(6, 1, 30, 30, 999.99),
(6, 19, 15, 15, 529.99),
(6, 16, 10, 10, 699.99),

-- SO-2024-007
(7, 2, 100, 100, 29.99),
(7, 4, 200, 200, 12.99),
(7, 5, 150, 150, 19.99),
(7, 7, 30, 30, 199.99),

-- SO-2024-008
(8, 1, 25, 0, 999.99),
(8, 3, 20, 0, 549.99),
(8, 14, 35, 0, 159.99),
(8, 15, 60, 0, 89.99),

-- SO-2024-009
(9, 6, 40, 0, 79.99),
(9, 7, 20, 0, 199.99),
(9, 11, 15, 0, 149.99),
(9, 13, 25, 0, 99.99),

-- SO-2024-010
(10, 9, 15, 0, 449.99),
(10, 10, 20, 0, 299.99),
(10, 16, 12, 0, 699.99),
(10, 19, 8, 0, 529.99);

-- ============================================================
-- 11. INSERT TRANSACTION HISTORY
-- ============================================================
INSERT INTO transaction_history (transaction_date, transaction_type, reference_number, product_id, warehouse_id, quantity_change, quantity_before, quantity_after, unit_cost, total_value, po_id, so_id, performed_by, notes) VALUES
-- Purchase transactions (Stock IN)
('2024-11-07 10:30:00', 'purchase', 'PO-2024-001', 1, 1, 50, 35, 85, 650.00, 32500.00, 1, NULL, 3, 'Received laptops from TechSupply Co.'),
('2024-11-07 10:35:00', 'purchase', 'PO-2024-001', 3, 1, 20, 145, 165, 320.00, 6400.00, 1, NULL, 3, 'Received monitors'),
('2024-11-18 14:20:00', 'purchase', 'PO-2024-002', 2, 2, 100, 45, 145, 15.00, 1500.00, 2, NULL, 4, 'Mice received'),
('2024-11-18 14:25:00', 'purchase', 'PO-2024-002', 6, 2, 50, 115, 165, 45.00, 2250.00, 2, NULL, 4, 'Webcams received'),

-- Sales transactions (Stock OUT)
('2024-11-04 09:15:00', 'sale', 'SO-2024-001', 1, 1, -5, 90, 85, 650.00, -3250.00, NULL, 1, 3, 'Shipped to ABC Corporation'),
('2024-11-04 09:20:00', 'sale', 'SO-2024-001', 2, 1, -20, 340, 320, 15.00, -300.00, NULL, 1, 3, 'Shipped to ABC Corporation'),
('2024-11-07 11:30:00', 'sale', 'SO-2024-002', 8, 2, -25, 190, 165, 75.00, -1875.00, NULL, 2, 4, 'Shipped to Tech Solutions'),
('2024-11-07 11:35:00', 'sale', 'SO-2024-002', 13, 2, -30, 125, 95, 60.00, -1800.00, NULL, 2, 4, 'Shipped hard drives'),

-- Adjustments
('2024-11-10 15:00:00', 'adjustment', 'ADJ-001', 8, 1, -2, 20, 18, 75.00, -150.00, NULL, NULL, 2, 'Damaged items found during inspection'),
('2024-11-15 10:00:00', 'adjustment', 'ADJ-002', 16, 3, -3, 15, 12, 420.00, -1260.00, NULL, NULL, 2, 'Quality issue - returned to supplier'),
('2024-11-20 16:30:00', 'adjustment', 'CYCLE-001', 4, 1, 5, 415, 420, 5.00, 25.00, NULL, NULL, 3, 'Cycle count correction - found extra units'),

-- More sales
('2024-11-24 13:45:00', 'sale', 'SO-2024-006', 1, 1, -30, 115, 85, 650.00, -19500.00, NULL, 6, 3, 'Government contract shipment'),
('2024-11-24 13:50:00', 'sale', 'SO-2024-006', 19, 1, -15, 53, 38, 320.00, -4800.00, NULL, 6, 3, 'CPUs shipped'),
('2024-11-26 10:00:00', 'sale', 'SO-2024-007', 2, 2, -100, 245, 145, 15.00, -1500.00, NULL, 7, 4, 'Retail chain restock'),
('2024-11-26 10:05:00', 'sale', 'SO-2024-007', 4, 2, -200, 292, 92, 5.00, -1000.00, NULL, 7, 4, 'USB cables bulk shipment'),

-- Returns
('2024-11-28 14:20:00', 'return', 'RET-001', 2, 1, 3, 317, 320, 15.00, 45.00, NULL, 1, 3, 'Customer return - unused items'),
('2024-11-30 11:15:00', 'return', 'RET-002', 8, 1, 2, 16, 18, 75.00, 150.00, NULL, 2, 3, 'Defective return from customer'),

-- Transfers between warehouses
('2024-12-01 09:00:00', 'transfer', 'TRF-001', 1, 1, -10, 95, 85, 650.00, -6500.00, NULL, NULL, 2, 'Transfer to Warehouse C'),
('2024-12-01 15:00:00', 'transfer', 'TRF-001', 1, 3, 10, 38, 48, 650.00, 6500.00, NULL, NULL, 3, 'Received from Warehouse A');

-- ============================================================
-- 12. INSERT STOCK ADJUSTMENTS
-- ============================================================
INSERT INTO stock_adjustments (adjustment_date, adjustment_type, product_id, warehouse_id, quantity_adjusted, reason, cost_impact, adjusted_by, approved_by) VALUES
('2024-11-10', 'damage', 8, 1, -2, 'Water damage discovered during routine inspection', -150.00, 3, 2),
('2024-11-15', 'write_off', 16, 3, -3, 'DOA units - manufacturer defect confirmed', -1260.00, 3, 1),
('2024-11-20', 'correction', 4, 1, 5, 'Cycle count revealed undocumented units', 25.00, 3, 2),
('2024-11-22', 'expired', 5, 2, -8, 'Cable lot failed quality check', -64.00, 4, 2),
('2024-11-25', 'found', 15, 1, 3, 'Misplaced inventory found in wrong location', 165.00, 3, 2),
('2024-11-28', 'theft', 19, 4, -2, 'Security review identified missing processors', -640.00, 4, 1),
('2024-12-02', 'correction', 10, 4, -1, 'Scanner unit was double-counted', -180.00, 4, 2);

-- ============================================================
-- 13. INSERT PRODUCT MOVEMENTS (Warehouse Transfers)
-- ============================================================
INSERT INTO product_movements (movement_date, product_id, from_warehouse_id, to_warehouse_id, quantity, status, initiated_by, received_by, notes) VALUES
('2024-11-15', 1, 1, 3, 10, 'received', 2, 3, 'Rebalancing stock levels'),
('2024-11-18', 13, 2, 4, 15, 'received', 2, 4, 'Transfer to meet regional demand'),
('2024-11-22', 16, 1, 2, 5, 'received', 2, 4, 'Graphics cards for west coast orders'),
('2024-11-25', 2, 2, 1, 30, 'received', 2, 3, 'Consolidating inventory'),
('2024-11-28', 14, 3, 4, 12, 'received', 2, 4, 'SSD transfer for upcoming orders'),
('2024-12-01', 1, 1, 3, 10, 'received', 2, 3, 'Laptop distribution'),
('2024-12-03', 7, 1, 2, 8, 'in_transit', 2, NULL, 'Headphones in transit'),
('2024-12-04', 19, 2, 3, 5, 'initiated', 2, NULL, 'CPU transfer pending');

-- ============================================================
-- DATA POPULATION COMPLETE
-- ============================================================

-- Verify data counts
SELECT 'users' as table_name, COUNT(*) as record_count FROM users
UNION ALL
SELECT 'categories', COUNT(*) FROM categories
UNION ALL
SELECT 'suppliers', COUNT(*) FROM suppliers
UNION ALL
SELECT 'warehouses', COUNT(*) FROM warehouses
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'inventory', COUNT(*) FROM inventory
UNION ALL
SELECT 'purchase_orders', COUNT(*) FROM purchase_orders
UNION ALL
SELECT 'purchase_order_items', COUNT(*) FROM purchase_order_items
UNION ALL
SELECT 'sales_orders', COUNT(*) FROM sales_orders
UNION ALL
SELECT 'sales_order_items', COUNT(*) FROM sales_order_items
UNION ALL
SELECT 'transaction_history', COUNT(*) FROM transaction_history
UNION ALL
SELECT 'stock_adjustments', COUNT(*) FROM stock_adjustments
UNION ALL
SELECT 'product_movements', COUNT(*) FROM product_movements;

-- Show current stock summary
SELECT 
    p.sku,
    p.product_name,
    SUM(i.quantity_on_hand) as total_stock,
    SUM(i.quantity_reserved) as reserved,
    SUM(i.quantity_available) as available,
    CASE 
        WHEN SUM(i.quantity_on_hand) < p.reorder_point * 0.5 THEN 'CRITICAL'
        WHEN SUM(i.quantity_on_hand) < p.reorder_point THEN 'LOW'
        ELSE 'OK'
    END as alert_status
FROM products p
LEFT JOIN inventory i ON p.product_id = i.product_id
GROUP BY p.product_id, p.sku, p.product_name, p.reorder_point
ORDER BY p.sku;
