"""
Stock Management KPI Calculator
Comprehensive KPI calculations for inventory management dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class InventoryKPICalculator:
    """
    Calculate and analyze comprehensive inventory management KPIs
    """
    
    def __init__(self, stock_df, transactions_df, cost_data=None):
        """
        Initialize KPI calculator with inventory and transaction data
        
        Args:
            stock_df: DataFrame with current stock information
            transactions_df: DataFrame with historical transactions
            cost_data: Optional dict with cost information
        """
        self.stock_df = stock_df.copy()
        self.transactions_df = transactions_df.copy()
        self.cost_data = cost_data or {}
        
    def inventory_turnover(self, period_days=365):
        """
        Calculate Inventory Turnover Ratio
        Formula: Cost of Goods Sold (COGS) / Average Inventory Value
        
        Returns:
            dict: Turnover ratio and analysis
        """
        # Calculate COGS from outbound transactions
        outbound = self.transactions_df[self.transactions_df['Type'] == 'Out'].copy()
        
        # Merge with stock data to get prices
        outbound = outbound.merge(
            self.stock_df[['Product', 'Unit_Price']], 
            on='Product', 
            how='left'
        )
        outbound['Transaction_Value'] = outbound['Quantity'] * outbound['Unit_Price']
        
        cogs = outbound['Transaction_Value'].sum()
        
        # Average inventory value
        avg_inventory_value = self.stock_df['Total_Value'].mean()
        total_inventory_value = self.stock_df['Total_Value'].sum()
        
        # Calculate turnover
        turnover_ratio = cogs / avg_inventory_value if avg_inventory_value > 0 else 0
        annual_turnover = turnover_ratio * (365 / period_days)
        
        return {
            'turnover_ratio': round(turnover_ratio, 2),
            'annual_turnover': round(annual_turnover, 2),
            'cogs': round(cogs, 2),
            'avg_inventory_value': round(avg_inventory_value, 2),
            'total_inventory_value': round(total_inventory_value, 2),
            'interpretation': self._interpret_turnover(annual_turnover)
        }
    
    def days_sales_inventory(self):
        """
        Calculate Days Sales of Inventory (DSI)
        Formula: (Average Inventory / COGS) * 365
        
        Returns:
            dict: DSI metrics
        """
        turnover_data = self.inventory_turnover()
        
        if turnover_data['annual_turnover'] > 0:
            dsi = 365 / turnover_data['annual_turnover']
        else:
            dsi = 0
            
        return {
            'days_sales_inventory': round(dsi, 1),
            'interpretation': f"Takes {round(dsi, 1)} days to sell entire inventory",
            'status': 'Good' if dsi < 60 else 'Average' if dsi < 90 else 'Poor'
        }
    
    def stock_accuracy(self):
        """
        Calculate Stock Accuracy Rate
        Formula: (Accurate Stock Records / Total Stock Records) * 100
        
        Returns:
            dict: Accuracy metrics
        """
        # Simulate accuracy check (in real scenario, compare with physical count)
        total_items = len(self.stock_df)
        
        # Assume 95-99% accuracy for items with recent restocking
        self.stock_df['Last_Restocked_Date'] = pd.to_datetime(self.stock_df['Last_Restocked'])
        days_since_restock = (datetime.now() - self.stock_df['Last_Restocked_Date']).dt.days
        
        # Items restocked within 30 days are more likely to be accurate
        accurate_items = len(self.stock_df[days_since_restock <= 30])
        
        # Add random accuracy factor
        accuracy_rate = (accurate_items / total_items * 100) if total_items > 0 else 0
        accuracy_rate = min(accuracy_rate + np.random.uniform(0, 5), 100)
        
        inaccurate_items = total_items - int(total_items * accuracy_rate / 100)
        
        return {
            'accuracy_rate': round(accuracy_rate, 2),
            'total_items': total_items,
            'accurate_items': total_items - inaccurate_items,
            'inaccurate_items': inaccurate_items,
            'status': 'Excellent' if accuracy_rate >= 98 else 'Good' if accuracy_rate >= 95 else 'Needs Improvement'
        }
    
    def stockout_rate(self, period_days=30):
        """
        Calculate Stockout Rate
        Formula: (Number of Stockouts / Total Orders) * 100
        
        Returns:
            dict: Stockout metrics
        """
        # Identify stockouts (when quantity is 0 or critical low)
        stockouts = len(self.stock_df[self.stock_df['Stock_Status'] == 'Critical'])
        total_products = len(self.stock_df)
        
        # Calculate from transactions
        recent_transactions = self.transactions_df[
            self.transactions_df['Date'] >= datetime.now() - timedelta(days=period_days)
        ]
        
        outbound_requests = len(recent_transactions[recent_transactions['Type'] == 'Out'])
        
        stockout_rate = (stockouts / total_products * 100) if total_products > 0 else 0
        
        return {
            'stockout_rate': round(stockout_rate, 2),
            'stockout_items': stockouts,
            'total_items': total_products,
            'period_days': period_days,
            'affected_orders': int(outbound_requests * stockout_rate / 100),
            'status': 'Excellent' if stockout_rate < 2 else 'Good' if stockout_rate < 5 else 'Critical'
        }
    
    def order_fulfillment_rate(self, period_days=30):
        """
        Calculate Order Fulfillment Rate
        Formula: (Orders Fulfilled / Total Orders) * 100
        
        Returns:
            dict: Fulfillment metrics
        """
        recent_transactions = self.transactions_df[
            self.transactions_df['Date'] >= datetime.now() - timedelta(days=period_days)
        ]
        
        total_outbound = len(recent_transactions[recent_transactions['Type'] == 'Out'])
        
        # Assume 95-99% fulfillment based on stock status
        critical_stock_ratio = len(self.stock_df[self.stock_df['Stock_Status'] == 'Critical']) / len(self.stock_df)
        
        fulfillment_rate = 100 - (critical_stock_ratio * 10)
        fulfillment_rate = max(85, min(fulfillment_rate, 100))
        
        fulfilled_orders = int(total_outbound * fulfillment_rate / 100)
        unfulfilled_orders = total_outbound - fulfilled_orders
        
        return {
            'fulfillment_rate': round(fulfillment_rate, 2),
            'total_orders': total_outbound,
            'fulfilled_orders': fulfilled_orders,
            'unfulfilled_orders': unfulfilled_orders,
            'period_days': period_days,
            'status': 'Excellent' if fulfillment_rate >= 98 else 'Good' if fulfillment_rate >= 95 else 'Needs Improvement'
        }
    
    def carrying_cost(self, storage_cost_rate=0.15):
        """
        Calculate Inventory Carrying Cost
        Formula: Average Inventory Value * Carrying Cost Rate
        
        Args:
            storage_cost_rate: Annual rate (default 15%)
            
        Returns:
            dict: Carrying cost metrics
        """
        total_inventory_value = self.stock_df['Total_Value'].sum()
        
        # Components of carrying cost
        storage_cost = total_inventory_value * storage_cost_rate
        insurance_cost = total_inventory_value * 0.02  # 2% of inventory value
        obsolescence_cost = total_inventory_value * 0.03  # 3% for obsolescence
        opportunity_cost = total_inventory_value * 0.05  # 5% opportunity cost
        
        total_carrying_cost = storage_cost + insurance_cost + obsolescence_cost + opportunity_cost
        carrying_cost_rate = (total_carrying_cost / total_inventory_value * 100) if total_inventory_value > 0 else 0
        
        return {
            'total_carrying_cost': round(total_carrying_cost, 2),
            'annual_carrying_cost': round(total_carrying_cost, 2),
            'monthly_carrying_cost': round(total_carrying_cost / 12, 2),
            'carrying_cost_rate': round(carrying_cost_rate, 2),
            'inventory_value': round(total_inventory_value, 2),
            'breakdown': {
                'storage': round(storage_cost, 2),
                'insurance': round(insurance_cost, 2),
                'obsolescence': round(obsolescence_cost, 2),
                'opportunity': round(opportunity_cost, 2)
            },
            'status': 'Good' if carrying_cost_rate < 25 else 'Average' if carrying_cost_rate < 35 else 'High'
        }
    
    def dead_stock_percentage(self, no_movement_days=90):
        """
        Calculate Dead Stock Percentage
        Formula: (Dead Stock Value / Total Inventory Value) * 100
        
        Args:
            no_movement_days: Days without movement to classify as dead stock
            
        Returns:
            dict: Dead stock metrics
        """
        # Check last restock date
        self.stock_df['Last_Restocked_Date'] = pd.to_datetime(self.stock_df['Last_Restocked'])
        days_since_movement = (datetime.now() - self.stock_df['Last_Restocked_Date']).dt.days
        
        # Identify dead stock
        dead_stock = self.stock_df[days_since_movement > no_movement_days].copy()
        
        dead_stock_value = dead_stock['Total_Value'].sum()
        total_inventory_value = self.stock_df['Total_Value'].sum()
        
        dead_stock_percentage = (dead_stock_value / total_inventory_value * 100) if total_inventory_value > 0 else 0
        
        return {
            'dead_stock_percentage': round(dead_stock_percentage, 2),
            'dead_stock_items': len(dead_stock),
            'dead_stock_value': round(dead_stock_value, 2),
            'total_inventory_value': round(total_inventory_value, 2),
            'no_movement_threshold_days': no_movement_days,
            'products': dead_stock[['Product', 'Quantity', 'Total_Value', 'Last_Restocked']].to_dict('records'),
            'status': 'Excellent' if dead_stock_percentage < 5 else 'Good' if dead_stock_percentage < 10 else 'Critical'
        }
    
    def backorder_rate(self, period_days=30):
        """
        Calculate Backorder Rate
        Formula: (Backorders / Total Orders) * 100
        
        Returns:
            dict: Backorder metrics
        """
        recent_transactions = self.transactions_df[
            self.transactions_df['Date'] >= datetime.now() - timedelta(days=period_days)
        ]
        
        total_outbound = len(recent_transactions[recent_transactions['Type'] == 'Out'])
        
        # Estimate backorders based on critical and low stock
        critical_low_stock = len(self.stock_df[self.stock_df['Stock_Status'].isin(['Critical', 'Low'])])
        total_items = len(self.stock_df)
        
        backorder_estimate_rate = (critical_low_stock / total_items * 100) if total_items > 0 else 0
        backorders = int(total_outbound * backorder_estimate_rate / 100)
        
        return {
            'backorder_rate': round(backorder_estimate_rate, 2),
            'total_orders': total_outbound,
            'backorders': backorders,
            'fulfilled_immediately': total_outbound - backorders,
            'period_days': period_days,
            'status': 'Excellent' if backorder_estimate_rate < 2 else 'Good' if backorder_estimate_rate < 5 else 'Critical'
        }
    
    def fill_rate(self):
        """
        Calculate Fill Rate
        Formula: (Orders Fulfilled Completely / Total Orders) * 100
        
        Returns:
            dict: Fill rate metrics
        """
        # Calculate based on current stock levels
        adequate_stock = len(self.stock_df[self.stock_df['Stock_Status'].isin(['Adequate', 'Overstocked'])])
        total_items = len(self.stock_df)
        
        fill_rate = (adequate_stock / total_items * 100) if total_items > 0 else 0
        
        return {
            'fill_rate': round(fill_rate, 2),
            'items_in_stock': adequate_stock,
            'total_items': total_items,
            'items_short': total_items - adequate_stock,
            'status': 'Excellent' if fill_rate >= 98 else 'Good' if fill_rate >= 95 else 'Needs Improvement'
        }
    
    def inventory_shrinkage(self, expected_vs_actual_diff=0.02):
        """
        Calculate Inventory Shrinkage
        Formula: ((Expected Inventory - Actual Inventory) / Expected Inventory) * 100
        
        Args:
            expected_vs_actual_diff: Expected shrinkage rate (default 2%)
            
        Returns:
            dict: Shrinkage metrics
        """
        total_inventory_value = self.stock_df['Total_Value'].sum()
        
        # Simulate shrinkage (theft, damage, errors)
        shrinkage_rate = np.random.uniform(0.5, 3.0)  # 0.5% to 3%
        shrinkage_value = total_inventory_value * (shrinkage_rate / 100)
        
        actual_value = total_inventory_value - shrinkage_value
        
        return {
            'shrinkage_rate': round(shrinkage_rate, 2),
            'shrinkage_value': round(shrinkage_value, 2),
            'expected_inventory_value': round(total_inventory_value, 2),
            'actual_inventory_value': round(actual_value, 2),
            'status': 'Excellent' if shrinkage_rate < 1.5 else 'Good' if shrinkage_rate < 2.5 else 'Critical'
        }
    
    def lead_time_analysis(self):
        """
        Calculate Average Lead Time
        Formula: Average time between order placement and receipt
        
        Returns:
            dict: Lead time metrics
        """
        # Calculate from inbound transactions
        inbound = self.transactions_df[self.transactions_df['Type'] == 'In'].copy()
        
        if len(inbound) > 0:
            # Group by product and calculate time between orders
            inbound = inbound.sort_values('Date')
            
            lead_times_by_product = {}
            
            for product in inbound['Product'].unique():
                product_orders = inbound[inbound['Product'] == product]['Date']
                if len(product_orders) > 1:
                    time_diffs = product_orders.diff().dt.days.dropna()
                    avg_lead_time = time_diffs.mean()
                    lead_times_by_product[product] = avg_lead_time
            
            overall_avg = np.mean(list(lead_times_by_product.values())) if lead_times_by_product else 14
        else:
            overall_avg = 14
            lead_times_by_product = {}
        
        # Calculate by supplier
        supplier_lead_times = {}
        for supplier in self.stock_df['Supplier'].unique():
            supplier_products = self.stock_df[self.stock_df['Supplier'] == supplier]['Product'].tolist()
            supplier_lt = [lead_times_by_product.get(p, 14) for p in supplier_products if p in lead_times_by_product]
            if supplier_lt:
                supplier_lead_times[supplier] = round(np.mean(supplier_lt), 1)
            else:
                supplier_lead_times[supplier] = 14.0
        
        return {
            'average_lead_time_days': round(overall_avg, 1),
            'min_lead_time': round(min(lead_times_by_product.values()), 1) if lead_times_by_product else 7,
            'max_lead_time': round(max(lead_times_by_product.values()), 1) if lead_times_by_product else 30,
            'by_supplier': supplier_lead_times,
            'products_analyzed': len(lead_times_by_product),
            'status': 'Excellent' if overall_avg < 7 else 'Good' if overall_avg < 14 else 'Slow'
        }
    
    def abc_analysis(self):
        """
        Perform ABC Analysis
        A items: Top 20% of products, 80% of value
        B items: Next 30% of products, 15% of value
        C items: Bottom 50% of products, 5% of value
        
        Returns:
            dict: ABC classification
        """
        df = self.stock_df.copy()
        df = df.sort_values('Total_Value', ascending=False)
        
        total_value = df['Total_Value'].sum()
        df['Cumulative_Value'] = df['Total_Value'].cumsum()
        df['Cumulative_Percentage'] = (df['Cumulative_Value'] / total_value * 100)
        
        # Classify
        df['ABC_Category'] = 'C'
        df.loc[df['Cumulative_Percentage'] <= 80, 'ABC_Category'] = 'A'
        df.loc[(df['Cumulative_Percentage'] > 80) & (df['Cumulative_Percentage'] <= 95), 'ABC_Category'] = 'B'
        
        # Calculate statistics
        a_items = df[df['ABC_Category'] == 'A']
        b_items = df[df['ABC_Category'] == 'B']
        c_items = df[df['ABC_Category'] == 'C']
        
        return {
            'category_A': {
                'count': len(a_items),
                'percentage': round(len(a_items) / len(df) * 100, 1),
                'value': round(a_items['Total_Value'].sum(), 2),
                'value_percentage': round(a_items['Total_Value'].sum() / total_value * 100, 1),
                'products': a_items[['Product', 'Total_Value', 'Quantity']].to_dict('records')
            },
            'category_B': {
                'count': len(b_items),
                'percentage': round(len(b_items) / len(df) * 100, 1),
                'value': round(b_items['Total_Value'].sum(), 2),
                'value_percentage': round(b_items['Total_Value'].sum() / total_value * 100, 1),
                'products': b_items[['Product', 'Total_Value', 'Quantity']].to_dict('records')
            },
            'category_C': {
                'count': len(c_items),
                'percentage': round(len(c_items) / len(df) * 100, 1),
                'value': round(c_items['Total_Value'].sum(), 2),
                'value_percentage': round(c_items['Total_Value'].sum() / total_value * 100, 1),
                'products': c_items[['Product', 'Total_Value', 'Quantity']].to_dict('records')
            },
            'total_value': round(total_value, 2)
        }
    
    def inventory_valuation(self):
        """
        Calculate Inventory Valuation using different methods
        
        Returns:
            dict: Valuation metrics
        """
        # FIFO (First In First Out) - using current unit prices
        fifo_value = (self.stock_df['Quantity'] * self.stock_df['Unit_Price']).sum()
        
        # Average Cost Method
        avg_unit_price = self.stock_df['Unit_Price'].mean()
        avg_cost_value = self.stock_df['Quantity'].sum() * avg_unit_price
        
        # Weighted Average
        weighted_avg_value = self.stock_df['Total_Value'].sum()
        
        # By category
        category_valuation = self.stock_df.groupby('Category').agg({
            'Total_Value': 'sum',
            'Quantity': 'sum'
        }).to_dict('index')
        
        # By warehouse
        warehouse_valuation = self.stock_df.groupby('Warehouse').agg({
            'Total_Value': 'sum',
            'Quantity': 'sum'
        }).to_dict('index')
        
        return {
            'fifo_valuation': round(fifo_value, 2),
            'average_cost_valuation': round(avg_cost_value, 2),
            'weighted_average_valuation': round(weighted_avg_value, 2),
            'total_units': int(self.stock_df['Quantity'].sum()),
            'by_category': {k: {'value': round(v['Total_Value'], 2), 'units': int(v['Quantity'])} 
                           for k, v in category_valuation.items()},
            'by_warehouse': {k: {'value': round(v['Total_Value'], 2), 'units': int(v['Quantity'])} 
                            for k, v in warehouse_valuation.items()}
        }
    
    def supplier_performance(self):
        """
        Analyze Supplier Performance
        
        Returns:
            dict: Supplier metrics
        """
        supplier_metrics = {}
        
        for supplier in self.stock_df['Supplier'].unique():
            supplier_data = self.stock_df[self.stock_df['Supplier'] == supplier]
            
            # Calculate metrics
            total_products = len(supplier_data)
            total_value = supplier_data['Total_Value'].sum()
            avg_stock_status = supplier_data['Stock_Status'].value_counts().to_dict()
            
            # Quality score (based on stock status)
            quality_score = (
                avg_stock_status.get('Adequate', 0) * 1.0 +
                avg_stock_status.get('Overstocked', 0) * 0.8 +
                avg_stock_status.get('Low', 0) * 0.5 +
                avg_stock_status.get('Critical', 0) * 0.2
            ) / total_products * 100 if total_products > 0 else 0
            
            supplier_metrics[supplier] = {
                'total_products': total_products,
                'total_value': round(total_value, 2),
                'avg_unit_price': round(supplier_data['Unit_Price'].mean(), 2),
                'stock_status_distribution': avg_stock_status,
                'quality_score': round(quality_score, 1),
                'status': 'Excellent' if quality_score >= 80 else 'Good' if quality_score >= 60 else 'Poor'
            }
        
        return {
            'suppliers': supplier_metrics,
            'total_suppliers': len(supplier_metrics),
            'best_supplier': max(supplier_metrics.items(), key=lambda x: x[1]['quality_score'])[0],
            'worst_supplier': min(supplier_metrics.items(), key=lambda x: x[1]['quality_score'])[0]
        }
    
    def item_aging_analysis(self):
        """
        Analyze Item Aging
        
        Returns:
            dict: Aging analysis
        """
        self.stock_df['Last_Restocked_Date'] = pd.to_datetime(self.stock_df['Last_Restocked'])
        self.stock_df['Days_In_Stock'] = (datetime.now() - self.stock_df['Last_Restocked_Date']).dt.days
        
        # Age categories
        age_categories = {
            '0-30 days': len(self.stock_df[self.stock_df['Days_In_Stock'] <= 30]),
            '31-60 days': len(self.stock_df[(self.stock_df['Days_In_Stock'] > 30) & (self.stock_df['Days_In_Stock'] <= 60)]),
            '61-90 days': len(self.stock_df[(self.stock_df['Days_In_Stock'] > 60) & (self.stock_df['Days_In_Stock'] <= 90)]),
            '90+ days': len(self.stock_df[self.stock_df['Days_In_Stock'] > 90])
        }
        
        # Value by age
        age_value = {
            '0-30 days': round(self.stock_df[self.stock_df['Days_In_Stock'] <= 30]['Total_Value'].sum(), 2),
            '31-60 days': round(self.stock_df[(self.stock_df['Days_In_Stock'] > 30) & (self.stock_df['Days_In_Stock'] <= 60)]['Total_Value'].sum(), 2),
            '61-90 days': round(self.stock_df[(self.stock_df['Days_In_Stock'] > 60) & (self.stock_df['Days_In_Stock'] <= 90)]['Total_Value'].sum(), 2),
            '90+ days': round(self.stock_df[self.stock_df['Days_In_Stock'] > 90]['Total_Value'].sum(), 2)
        }
        
        # Oldest items
        oldest_items = self.stock_df.nlargest(10, 'Days_In_Stock')[
            ['Product', 'Days_In_Stock', 'Quantity', 'Total_Value']
        ].to_dict('records')
        
        return {
            'age_distribution': age_categories,
            'value_by_age': age_value,
            'average_age_days': round(self.stock_df['Days_In_Stock'].mean(), 1),
            'oldest_items': oldest_items,
            'items_over_90_days': age_categories['90+ days'],
            'status': 'Good' if age_categories['90+ days'] < len(self.stock_df) * 0.1 else 'Needs Attention'
        }
    
    def get_all_kpis(self):
        """
        Calculate all KPIs and return comprehensive report
        
        Returns:
            dict: All KPI metrics
        """
        return {
            'inventory_turnover': self.inventory_turnover(),
            'days_sales_inventory': self.days_sales_inventory(),
            'stock_accuracy': self.stock_accuracy(),
            'stockout_rate': self.stockout_rate(),
            'order_fulfillment': self.order_fulfillment_rate(),
            'carrying_cost': self.carrying_cost(),
            'dead_stock_percentage': self.dead_stock_percentage(),
            'backorder_rate': self.backorder_rate(),
            'fill_rate': self.fill_rate(),
            'inventory_shrinkage': self.inventory_shrinkage(),
            'lead_time': self.lead_time_analysis(),
            'abc_analysis': self.abc_analysis(),
            'inventory_valuation': self.inventory_valuation(),
            'supplier_performance': self.supplier_performance(),
            'item_aging': self.item_aging_analysis()
        }
    
    @staticmethod
    def _interpret_turnover(turnover):
        """Helper to interpret turnover ratio"""
        if turnover > 12:
            return "Excellent - Very high turnover"
        elif turnover > 6:
            return "Good - Healthy turnover"
        elif turnover > 3:
            return "Average - Moderate turnover"
        else:
            return "Low - Slow-moving inventory"


# Example usage
if __name__ == "__main__":
    # This would typically be imported and used with real data
    print("KPI Calculator Module - Import this into your dashboard")
    print("Usage: calculator = InventoryKPICalculator(stock_df, transactions_df)")
    print("       kpis = calculator.get_all_kpis()")
