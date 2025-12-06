"""
Database connection and data access module.
Handles: PostgreSQL connection, queries, and data retrieval
"""

import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from contextlib import contextmanager
from config import APP_CONFIG


class DatabaseConnection:
    """Manages PostgreSQL database connections and queries"""
    
    def __init__(self, db_config=None):
        """Initialize database connection with configuration"""
        self.db_config = db_config or {
            'host': 'localhost',
            'port': 5432,
            'database': 'stock_management',
            'user': 'postgres',
            'password': 'your_password'
        }
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = None
        try:
            conn = psycopg2.connect(**self.db_config)
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
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
        """Get current stock levels across all warehouses"""
        query = """
        SELECT 
            p.product_id,
            p.sku,
            p.product_name as "Product",
            c.category_name as "Category",
            SUM(i.quantity_on_hand) as "Quantity",
            SUM(i.quantity_reserved) as "Reserved",
            SUM(i.quantity_available) as "Available",
            p.reorder_point as "Reorder_Level",
            p.cost_price as "Unit_Price",
            p.selling_price as "Selling_Price",
            SUM(i.quantity_on_hand * p.cost_price) as "Total_Value",
            CASE 
                WHEN SUM(i.quantity_on_hand) < p.reorder_point * 0.5 THEN 'Critical'
                WHEN SUM(i.quantity_on_hand) < p.reorder_point THEN 'Low'
                WHEN SUM(i.quantity_on_hand) < p.reorder_point * 2 THEN 'Adequate'
                ELSE 'Overstocked'
            END as "Stock_Status",
            MAX(w.warehouse_name) as "Warehouse",
            MAX(s.supplier_name) as "Supplier",
            MAX(i.last_restocked_date) as "Last_Restocked",
            MAX(i.expiry_date) as "Expiry_Date"
        FROM products p
        LEFT JOIN inventory i ON p.product_id = i.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN warehouses w ON i.warehouse_id = w.warehouse_id
        LEFT JOIN suppliers s ON s.supplier_id = (
            SELECT po.supplier_id 
            FROM purchase_orders po
            JOIN purchase_order_items poi ON po.po_id = poi.po_id
            WHERE poi.product_id = p.product_id
            ORDER BY po.order_date DESC
            LIMIT 1
        )
        WHERE p.is_active = TRUE
        GROUP BY p.product_id, p.sku, p.product_name, c.category_name, 
                 p.reorder_point, p.cost_price, p.selling_price
        ORDER BY p.sku;
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
            i.quantity_available as "Available",
            i.stock_status as "Status",
            i.bin_location as "Location"
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN warehouses w ON i.warehouse_id = w.warehouse_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.is_active = TRUE
        """
        
        if warehouse_id:
            query += " AND i.warehouse_id = %s"
            return self.db.execute_query(query, (warehouse_id,))
        
        return self.db.execute_query(query)
    
    def get_transaction_history(self, days=30, transaction_type=None):
        """Get transaction history for specified period"""
        query = """
        SELECT 
            th.transaction_date as "Date",
            th.transaction_type as "Type",
            p.product_name as "Product",
            c.category_name as "Category",
            w.warehouse_name as "Warehouse",
            th.quantity_change as "Quantity",
            th.unit_cost as "Unit_Cost",
            th.total_value as "Total_Value",
            th.reference_number as "Reference",
            u.username as "User"
        FROM transaction_history th
        JOIN products p ON th.product_id = p.product_id
        JOIN warehouses w ON th.warehouse_id = w.warehouse_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN users u ON th.performed_by = u.user_id
        WHERE th.transaction_date >= CURRENT_DATE - INTERVAL '%s days'
        """
        
        params = [days]
        
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
            SUM(i.quantity_on_hand) as "Current_Stock",
            p.reorder_point as "Reorder_Point",
            p.reorder_quantity as "Reorder_Quantity",
            s.supplier_name as "Supplier",
            s.lead_time_days as "Lead_Time"
        FROM products p
        LEFT JOIN inventory i ON p.product_id = i.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        LEFT JOIN suppliers s ON s.supplier_id = (
            SELECT po.supplier_id 
            FROM purchase_orders po
            JOIN purchase_order_items poi ON po.po_id = poi.po_id
            WHERE poi.product_id = p.product_id
            ORDER BY po.order_date DESC
            LIMIT 1
        )
        WHERE p.is_active = TRUE
        GROUP BY p.product_id, p.sku, p.product_name, c.category_name, 
                 p.reorder_point, p.reorder_quantity, s.supplier_name, s.lead_time_days
        HAVING SUM(i.quantity_on_hand) < p.reorder_point
        ORDER BY (SUM(i.quantity_on_hand)::float / NULLIF(p.reorder_point, 0)) ASC;
        """
        return self.db.execute_query(query)
    
    def get_expiring_products(self, days=90):
        """Get products expiring within specified days"""
        query = """
        SELECT 
            p.sku as "SKU",
            p.product_name as "Product",
            w.warehouse_name as "Warehouse",
            i.quantity_on_hand as "Quantity",
            i.batch_number as "Batch",
            i.expiry_date as "Expiry_Date",
            EXTRACT(DAY FROM (i.expiry_date - CURRENT_DATE)) as "Days_Until_Expiry",
            (i.quantity_on_hand * p.cost_price) as "Value_At_Risk"
        FROM inventory i
        JOIN products p ON i.product_id = p.product_id
        JOIN warehouses w ON i.warehouse_id = w.warehouse_id
        WHERE i.expiry_date IS NOT NULL
          AND i.expiry_date <= CURRENT_DATE + INTERVAL '%s days'
          AND i.quantity_on_hand > 0
        ORDER BY i.expiry_date ASC;
        """
        return self.db.execute_query(query, (days,))
    
    def get_abc_analysis_data(self):
        """Get data for ABC analysis"""
        query = """
        SELECT 
            p.product_id,
            p.sku,
            p.product_name as "Product",
            c.category_name as "Category",
            SUM(i.quantity_on_hand) as quantity,
            p.cost_price as unit_value,
            SUM(i.quantity_on_hand * p.cost_price) as total_value,
            p.abc_classification as "ABC_Class"
        FROM products p
        LEFT JOIN inventory i ON p.product_id = i.product_id
        LEFT JOIN categories c ON p.category_id = c.category_id
        WHERE p.is_active = TRUE
        GROUP BY p.product_id, p.sku, p.product_name, c.category_name, 
                 p.cost_price, p.abc_classification
        ORDER BY total_value DESC;
        """
        return self.db.execute_query(query)
    
    def get_supplier_performance(self):
        """Get supplier performance metrics"""
        query = """
        SELECT 
            s.supplier_name as "Supplier",
            COUNT(DISTINCT po.po_id) as "Total_Orders",
            SUM(CASE WHEN po.status = 'received' THEN 1 ELSE 0 END) as "Completed_Orders",
            ROUND(AVG(EXTRACT(DAY FROM (po.actual_delivery_date - po.expected_delivery_date))), 1) as "Avg_Delay_Days",
            ROUND(100.0 * SUM(CASE WHEN po.actual_delivery_date <= po.expected_delivery_date THEN 1 ELSE 0 END) / 
                  NULLIF(COUNT(CASE WHEN po.actual_delivery_date IS NOT NULL THEN 1 END), 0), 1) as "OnTime_Percentage",
            SUM(po.total_amount) as "Total_Value",
            s.rating as "Rating",
            s.lead_time_days as "Lead_Time"
        FROM suppliers s
        LEFT JOIN purchase_orders po ON s.supplier_id = po.supplier_id
        WHERE s.is_active = TRUE
        GROUP BY s.supplier_id, s.supplier_name, s.rating, s.lead_time_days
        HAVING COUNT(DISTINCT po.po_id) > 0
        ORDER BY "OnTime_Percentage" DESC;
        """
        return self.db.execute_query(query)
    
    def insert_transaction(self, transaction_data):
        """Insert a new transaction record"""
        query = """
        INSERT INTO transaction_history 
        (transaction_type, reference_number, product_id, warehouse_id, 
         quantity_change, unit_cost, total_value, performed_by, notes)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
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
            transaction_data.get('user_id'),
            transaction_data.get('notes')
        )
        
        return self.db.execute_insert(query, params)
    
    def update_inventory_quantity(self, product_id, warehouse_id, quantity_change):
        """Update inventory quantity"""
        query = """
        UPDATE inventory
        SET quantity_on_hand = quantity_on_hand + %s,
            last_movement_date = CURRENT_DATE,
            updated_at = CURRENT_TIMESTAMP
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
        """
        
        if not include_inactive:
            query += " WHERE p.is_active = TRUE"
        
        query += " ORDER BY p.sku"
        
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
        (sku, product_name, description, category_id, cost_price, selling_price,
         reorder_point, reorder_quantity, weight_kg, unit_of_measure)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING product_id;
        """
        
        params = (
            product_data['sku'],
            product_data['name'],
            product_data.get('description'),
            product_data.get('category_id'),
            product_data['cost_price'],
            product_data['selling_price'],
            product_data.get('reorder_point', 10),
            product_data.get('reorder_quantity', 50),
            product_data.get('weight_kg'),
            product_data.get('unit_of_measure', 'pieces')
        )
        
        return self.db.execute_insert(query, params)
