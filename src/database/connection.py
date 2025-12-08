"""
Database connection and data access module.
Handles: PostgreSQL connection, queries, and data retrieval
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
import os
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseConnection:
    """Manages PostgreSQL database connections and queries"""
    
    def __init__(self, db_config=None):
        """Initialize database connection with configuration"""
        if db_config is None:
            # Load from environment variables with fallback defaults
            self.db_config = {
                # 'host': os.getenv('DB_HOST',= 'localhost'),
                # 'port': int(os.getenv('DB_PORT', '5432')),
                # 'database': os.getenv('DB_NAME', 'stock_management'),
                # 'user': os.getenv('DB_USER', 'postgres'),
                # 'password': os.getenv('DB_PASSWORD', 'my_password')
                'host':  'localhost',
                'port': 5432,
                'database': 'stock_management',
                'user': 'postgres',
                'password': 'my_password'
            }
            
            # Debug: Print loaded config (mask password)
            # print(f"📋 Database Config Loaded:")
            # print(f"   Host: {self.db_config['host']}")
            # print(f"   Port: {self.db_config['port']}")
            # print(f"   Database: {self.db_config['database']}")
            # print(f"   User: {self.db_config['user']}")
            # print(f"   Password: {'*' * len(str(self.db_config['password']))}")
        else:
            self.db_config = db_config
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            print(f"🔌 Attempting connection to {self.db_config['host']}:{self.db_config['port']}...")
            conn = psycopg2.connect(**self.db_config)
            print("✅ Connection successful!")
            yield conn
            conn.commit()
        except psycopg2.OperationalError as e:
            if conn:
                conn.rollback()
            print(f"❌ Connection failed: {str(e)}")
            print("\n💡 Common issues:")
            print("   1. Container not running: docker ps | findstr postgres")
            print("   2. Wrong password in .env file")
            print("   3. Database doesn't exist: docker exec -it postgres-stocl psql -U postgres -l")
            print("   4. Port not exposed: docker port postgres-stocl")
            raise
        except Exception as e:
            if conn:
                conn.rollback()
            print(f"❌ Unexpected error: {str(e)}")
            raise
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query, params=None):
        """Execute a query and return results as DataFrame"""
        with self.get_connection() as conn:
            return pd.read_sql_query(query, conn, params=params)
    
    def execute_insert(self, query, params=None):
        """Execute an insert/update/delete query"""
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                return cur.rowcount


class StockDataAccess:
    """Data access layer for stock management queries"""
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
    
    def get_current_stock_summary(self):
        """Get current stock levels - one row per product per warehouse"""
        query = """
        SELECT 
            p.product_id,
            p.sku,
            p.product_name as "Product",
            c.category_name as "Category",
            w.warehouse_name as "Warehouse",
            COALESCE(i.quantity_on_hand, 0) as "Quantity",
            COALESCE(i.quantity_reserved, 0) as "Reserved",
            COALESCE(i.quantity_on_hand - i.quantity_reserved, 0) as "Available",
            p.reorder_point as "Reorder_Level",
            p.cost_price as "Unit_Price",
            p.selling_price as "Selling_Price",
            COALESCE(i.quantity_on_hand * p.cost_price, 0) as "Total_Value",
            COALESCE(i.stock_status, 
                CASE 
                    WHEN COALESCE(i.quantity_on_hand, 0) = 0 THEN 'Out of Stock'
                    WHEN COALESCE(i.quantity_on_hand, 0) < p.reorder_point * 0.5 THEN 'Critical'
                    WHEN COALESCE(i.quantity_on_hand, 0) < p.reorder_point THEN 'Low'
                    WHEN COALESCE(i.quantity_on_hand, 0) < p.reorder_point * 2 THEN 'Adequate'
                    ELSE 'Overstocked'
                END
            ) as "Stock_Status",
            s.supplier_name as "Supplier",
            COALESCE(i.last_restocked_date, CURRENT_DATE - INTERVAL '90 days') as "Last_Restocked",
            NULL as "Expiry_Date"
        FROM products p
        CROSS JOIN warehouses w
        LEFT JOIN inventory i ON p.product_id = i.product_id AND w.warehouse_id = i.warehouse_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN suppliers s ON s.supplier_id = i.supplier_id
        WHERE p.is_active = TRUE AND w.is_active = TRUE
        ORDER BY p.sku, w.warehouse_name;
        """
        return self.db.execute_query(query)
    
    def get_stock_by_warehouse(self, warehouse_id=None):
        """Get stock levels by warehouse"""
        query = """
        SELECT 
            w.warehouse_name as "Warehouse",
            p.sku as "SKU",
            p.product_name as "Product",
            c.category_name as "Category",
            i.quantity_on_hand as "Quantity",
            i.quantity_reserved as "Reserved",
            (i.quantity_on_hand - i.quantity_reserved) as "Available",
            COALESCE(i.stock_status,
                CASE 
                    WHEN i.quantity_on_hand = 0 THEN 'Out of Stock'
                    WHEN i.quantity_on_hand < p.reorder_point * 0.5 THEN 'Critical'
                    WHEN i.quantity_on_hand < p.reorder_point THEN 'Low'
                    ELSE 'Adequate'
                END
            ) as "Status",
            i.bin_location as "Location"
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN warehouses w ON i.warehouse_id = w.warehouse_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.is_active = TRUE AND w.is_active = TRUE
        """
        
        if warehouse_id:
            query += " AND i.warehouse_id = %s"
            return self.db.execute_query(query, (warehouse_id,))
        
        return self.db.execute_query(query)
    
    def get_transaction_history(self, days=None, transaction_type=None):
        """Get transaction history for specified period"""
        query = """
        SELECT 
            th.transaction_date as "Date",
            CASE 
                WHEN th.transaction_type = 'purchase' THEN 'In'
                WHEN th.transaction_type = 'sale' THEN 'Out'
                ELSE 'Adjustment'
            END as "Type",
            p.product_name as "Product",
            c.category_name as "Category",
            w.warehouse_name as "Warehouse",
            ABS(th.quantity_change) as "Quantity",
            th.unit_cost as "Unit_Cost",
            ABS(th.total_value) as "Total_Value",
            th.reference_number as "Reference",
            u.username as "User"
        FROM transaction_history th
        JOIN products p ON th.product_id = p.product_id
        JOIN warehouses w ON th.warehouse_id = w.warehouse_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN users u ON th.performed_by = u.user_id
        WHERE 1=1
        """
        
        params = []
        
        if days is not None:
            query += " AND th.transaction_date >= CURRENT_DATE - CAST(%s || ' days' AS INTERVAL)"
            params.append(days)
        
        if transaction_type:
            query += " AND th.transaction_type = %s"
            params.append(transaction_type)
        
        query += " ORDER BY th.transaction_date DESC LIMIT 500"
        
        return self.db.execute_query(query, tuple(params))
    def get_low_stock_items(self):
        """Get products below reorder point"""
        query = """
        SELECT 
            p.sku as "SKU",
            p.product_name as "Product",
            c.category_name as "Category",
            SUM(COALESCE(i.quantity_on_hand, 0)) as "Current_Stock",
            p.reorder_point as "Reorder_Point",
            p.reorder_quantity as "Reorder_Quantity",
            s.supplier_name as "Supplier",
            s.lead_time_days as "Lead_Time"
        FROM products p
        LEFT JOIN inventory i ON p.product_id = i.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN suppliers s ON s.supplier_id = (
            SELECT i2.supplier_id 
            FROM inventory i2
            WHERE i2.product_id = p.product_id
            ORDER BY i2.last_restocked_date DESC
            LIMIT 1
        )
        WHERE p.is_active = TRUE
        GROUP BY p.product_id, p.sku, p.product_name, c.category_name, 
                 p.reorder_point, p.reorder_quantity, s.supplier_name, s.lead_time_days
        HAVING SUM(COALESCE(i.quantity_on_hand, 0)) < p.reorder_point
        ORDER BY (SUM(COALESCE(i.quantity_on_hand, 0))::float / NULLIF(p.reorder_point, 0)) ASC;
        """
        return self.db.execute_query(query)
    
    def get_expiring_products(self, days=90):
        """Get products expiring within specified days - Not available in minimal schema"""
        # Return empty dataframe as minimal schema doesn't track expiry dates
        return pd.DataFrame(columns=['SKU', 'Product', 'Warehouse', 'Quantity', 'Batch', 'Expiry_Date', 'Days_Until_Expiry', 'Value_At_Risk'])
    
    def get_abc_analysis_data(self):
        """Get data for ABC analysis"""
        query = """
        SELECT 
            p.product_id,
            p.sku,
            p.product_name as "Product",
            c.category_name as "Category",
            SUM(COALESCE(i.quantity_on_hand, 0)) as quantity,
            p.cost_price as unit_value,
            SUM(COALESCE(i.quantity_on_hand, 0) * p.cost_price) as total_value
        FROM products p
        LEFT JOIN inventory i ON p.product_id = i.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        GROUP BY p.product_id, p.sku, p.product_name, c.category_name, p.cost_price
        ORDER BY total_value DESC;
        """
        return self.db.execute_query(query)
    
    def get_supplier_performance(self):
        """Get supplier performance metrics - Not available in minimal schema"""
        # Return empty dataframe as minimal schema doesn't track purchase orders
        return pd.DataFrame(columns=['Supplier', 'Total_Orders', 'Completed_Orders', 'Avg_Delay_Days', 'OnTime_Percentage', 'Total_Value', 'Rating', 'Lead_Time'])
    
    def insert_transaction(self, transaction_data):
        """Insert a new transaction record"""
        query = """
        INSERT INTO transaction_history 
        (transaction_date, transaction_type, reference_number, product_id, warehouse_id, 
         quantity_change, unit_cost, total_value, performed_by)
        VALUES (CURRENT_DATE, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING transaction_id;
        """
        
        params = (
            transaction_data['type'],
            transaction_data['reference'],
            transaction_data['product_id'],
            transaction_data['warehouse_id'],
            transaction_data['quantity_change'],
            transaction_data.get('unit_cost'),
            transaction_data.get('total_value'),
            transaction_data.get('user_id')
        )
        
        return self.db.execute_insert(query, params)
    
    def update_inventory_quantity(self, product_id, warehouse_id, quantity_change):
        """Update inventory quantity"""
        query = """
        UPDATE inventory
        SET quantity_on_hand = quantity_on_hand + %s
        WHERE product_id = %s AND warehouse_id = %s
        RETURNING quantity_on_hand;
        """
        
        return self.db.execute_insert(query, (quantity_change, product_id, warehouse_id))


class ProductDataAccess:
    """Data access layer for product operations"""
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
    
    def get_all_products(self, include_inactive=False):
        """Get all products"""
        query = """
        SELECT 
            p.*,
            c.category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        ORDER BY p.sku
        """
        
        return self.db.execute_query(query)
    
    def get_product_by_sku(self, sku):
        """Get product details by SKU"""
        query = """
        SELECT 
            p.*,
            c.category_name,
            SUM(i.quantity_on_hand) as total_stock
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN inventory i ON p.product_id = i.product_id
        WHERE p.sku = %s
        GROUP BY p.product_id, c.category_name;
        """
        
        return self.db.execute_query(query, (sku,))
    
    def add_product(self, product_data):
        """Add a new product"""
        query = """
        INSERT INTO products 
        (sku, product_name, category_id, cost_price, selling_price)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING product_id;
        """
        
        params = (
            product_data['sku'],
            product_data['name'],
            product_data.get('category_id'),
            product_data['cost_price'],
            product_data['selling_price']
        )
        
        return self.db.execute_insert(query, params)
