# Database Setup Guide

## 📋 Prerequisites

1. **Install PostgreSQL** (version 12 or higher)
   - Download from: https://www.postgresql.org/download/
   - Or use Docker: `docker run --name postgres-stock -e POSTGRES_PASSWORD=your_password -p 5432:5432 -d postgres`

2. **Install Python PostgreSQL driver**
   ```powershell
   pip install psycopg2-binary
   ```

## 🚀 Setup Instructions

### Step 1: Create Database

Open PostgreSQL command line (psql) or pgAdmin and run:

```sql
CREATE DATABASE stock_management;
```

### Step 2: Execute Schema

Connect to the database and run the schema file:

**Using psql:**
```powershell
psql -U postgres -d stock_management -f database_schema.sql
```

**Using pgAdmin:**
1. Right-click on the database
2. Select "Query Tool"
3. Open `database_schema.sql`
4. Execute (F5)

### Step 3: Verify Installation

Check if tables were created:

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

You should see:
- users
- categories
- suppliers
- warehouses
- products
- inventory
- purchase_orders
- purchase_order_items
- sales_orders
- sales_order_items
- transaction_history
- stock_adjustments
- product_movements

### Step 4: Configure Connection

Update `database.py` with your credentials:

```python
db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'stock_management',
    'user': 'postgres',
    'password': 'your_password_here'  # Change this!
}
```

### Step 5: Test Connection

```python
from database import DatabaseConnection, StockDataAccess

# Test connection
db = DatabaseConnection(db_config)
stock_access = StockDataAccess(db)

# Try to fetch data
df = stock_access.get_current_stock_summary()
print(df.head())
```

## 📊 Database Schema Overview

### Core Tables:

1. **products** - Master product catalog
2. **inventory** - Current stock levels per warehouse
3. **transaction_history** - Complete audit trail
4. **purchase_orders** - Supplier orders
5. **sales_orders** - Customer orders
6. **warehouses** - Storage locations
7. **suppliers** - Vendor information
8. **categories** - Product classification

### Views (Pre-built Queries):

- `v_current_stock_summary` - Stock overview
- `v_stock_by_warehouse` - Warehouse inventory
- `v_recent_transactions` - Latest movements
- `v_expiring_products` - Items expiring soon
- `v_low_stock_alert` - Reorder alerts

## 🔄 Migration from Mock Data

To populate the database with initial data matching your mock data structure:

```sql
-- Insert products (matching your 20 mock products)
INSERT INTO products (sku, product_name, category_id, cost_price, selling_price, reorder_point)
SELECT 
    'SKU-' || (1000 + generate_series(1, 20)),
    product_names[generate_series(1, 20)],
    (SELECT category_id FROM categories ORDER BY RANDOM() LIMIT 1),
    (RANDOM() * 990 + 10)::DECIMAL(10,2),
    (RANDOM() * 1500 + 100)::DECIMAL(10,2),
    (RANDOM() * 80 + 20)::INT
FROM (VALUES 
    (ARRAY['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'USB Cable', 'HDMI Cable',
           'Webcam', 'Headphones', 'Printer', 'Scanner', 'Router', 'Switch',
           'Hard Drive', 'SSD', 'RAM Module', 'Graphics Card', 'Motherboard',
           'Power Supply', 'CPU', 'Cooling Fan'])
) AS t(product_names);

-- Insert inventory for each product in each warehouse
INSERT INTO inventory (product_id, warehouse_id, quantity_on_hand, stock_status)
SELECT 
    p.product_id,
    w.warehouse_id,
    (RANDOM() * 490 + 10)::INT,
    CASE 
        WHEN RANDOM() < 0.2 THEN 'critical'
        WHEN RANDOM() < 0.4 THEN 'low'
        WHEN RANDOM() < 0.8 THEN 'adequate'
        ELSE 'overstocked'
    END
FROM products p
CROSS JOIN warehouses w
WHERE p.is_active = TRUE;
```

## 🔗 Integrating with Dashboard

Update your `app.py` to use database instead of mock data:

```python
from database import DatabaseConnection, StockDataAccess

# Replace DataGenerator with database access
db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'stock_management',
    'user': 'postgres',
    'password': 'your_password'
}

db = DatabaseConnection(db_config)
stock_access = StockDataAccess(db)

# Get data from database
df = stock_access.get_current_stock_summary()
df_transactions = stock_access.get_transaction_history(days=30)
```

## 🛠️ Useful SQL Queries

### Check total inventory value:
```sql
SELECT SUM(quantity_on_hand * cost_price) as total_value
FROM inventory i
JOIN products p ON i.product_id = p.product_id;
```

### Get products by category:
```sql
SELECT c.category_name, COUNT(*) as product_count, 
       SUM(i.quantity_on_hand) as total_quantity
FROM products p
JOIN categories c ON p.category_id = c.category_id
LEFT JOIN inventory i ON p.product_id = i.product_id
GROUP BY c.category_name;
```

### Recent transactions summary:
```sql
SELECT 
    transaction_type,
    COUNT(*) as count,
    SUM(ABS(quantity_change)) as total_quantity,
    SUM(total_value) as total_value
FROM transaction_history
WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY transaction_type;
```

## 📝 Notes

- The schema includes **triggers** that automatically:
  - Update inventory quantities after transactions
  - Recalculate stock status when quantities change
  
- **Indexes** are created for optimal query performance on:
  - SKU lookups
  - Transaction history searches
  - Inventory status filtering
  
- **Views** provide pre-optimized queries for common dashboard needs

## 🔒 Security Considerations

1. Change default passwords
2. Create role-based users:
   ```sql
   CREATE USER dashboard_app WITH PASSWORD 'secure_password';
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO dashboard_app;
   ```

3. Use environment variables for credentials:
   ```python
   import os
   db_config = {
       'password': os.getenv('DB_PASSWORD')
   }
   ```

## 🐛 Troubleshooting

**Connection refused:**
- Check PostgreSQL is running: `pg_ctl status`
- Verify port 5432 is open
- Check pg_hba.conf allows local connections

**Permission denied:**
- Grant user permissions: `GRANT ALL PRIVILEGES ON DATABASE stock_management TO your_user;`

**Slow queries:**
- Run ANALYZE: `ANALYZE;`
- Check indexes: `SELECT * FROM pg_indexes WHERE schemaname = 'public';`
