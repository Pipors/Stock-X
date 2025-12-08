// Stock Dashboard Application - Main Entry Point
// Uses modular JS files: api.js, charts.js, components.js, table.js, modal.js
// static/js/app.js

class StockDashboardApp {
    constructor() {
        this.data = null;
        this.activeTab = 'stock-overview';
        this.sidebarOpen = false;
        this.init();
    }

    async init() {
        console.log('🚀 Initializing Stock Dashboard...');
        this.setupEventListeners();
        await this.loadDashboardData();
        setInterval(() => this.refreshData(), 60000);
        console.log('✅ Dashboard initialized');
    }

    setupEventListeners() {
        document.getElementById('hamburger-btn')?.addEventListener('click', () => this.toggleSidebar());
        document.getElementById('sidebar-overlay')?.addEventListener('click', () => this.closeSidebar());

        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                this.navigateToTab(btn.dataset.tab);
                this.closeSidebar();
            });
        });

        document.getElementById('kpi-modal')?.addEventListener('click', (e) => {
            if (e.target.id === 'kpi-modal' || e.target.classList.contains('kpi-modal-wrapper')) {
                KpiModal.close();
            }
        });
    }

    // Navigation
    toggleSidebar() { this.sidebarOpen ? this.closeSidebar() : this.openSidebar(); }
    openSidebar() {
        document.getElementById('sidebar')?.classList.add('open');
        document.getElementById('sidebar-overlay')?.classList.add('show');
        this.sidebarOpen = true;
    }
    closeSidebar() {
        document.getElementById('sidebar')?.classList.remove('open');
        document.getElementById('sidebar-overlay')?.classList.remove('show');
        this.sidebarOpen = false;
    }

    navigateToTab(tab) {
        this.activeTab = tab;
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.tab === tab);
        });
        this.renderCurrentTab();
    }

    // Data Loading
    async loadDashboardData() {
        this.showLoading(true);
        try {
            this.data = await ApiService.getDashboardData();
            this.updateLastUpdated(this.data.summary.last_updated);
            this.renderCurrentTab();
        } catch (error) {
            this.showError('Failed to load dashboard data');
        } finally {
            this.showLoading(false);
        }
    }

    async refreshData() {
        try {
            this.data = await ApiService.getDashboardData(true);
            this.updateLastUpdated(this.data.summary.last_updated);
            this.renderCurrentTab();
        } catch (error) {
            console.error('Refresh failed:', error);
        }
    }

    // Tab Rendering
    renderCurrentTab() {
        if (!this.data) return;
        const container = document.getElementById('tab-content');
        switch (this.activeTab) {
            case 'stock-overview': this.renderStockOverview(container); break;
            case 'kpis': this.renderKPIMetrics(container); break;
            case 'analytics': this.renderAnalytics(container); break;
            case 'forecasting': this.renderForecasting(container); break;
            case 'details': this.renderDetails(container); break;
        }
    }

    // ===== STOCK OVERVIEW TAB =====
    renderStockOverview(container) {
        const { stock } = this.data;
        const stats = this.calculateStats(stock);

        container.innerHTML = `
            ${Components.section('📦 Quick Stats', `
                <div class="kpi-row">
                    ${Components.quickStatCard('Total Products', stock.length, `${stats.totalQuantity.toLocaleString()} Units`, '📦', '#58a6ff')}
                    ${Components.quickStatCard('Total Value', `$${stats.totalValue.toLocaleString()}`, `Avg: $${Math.round(stats.totalValue / stock.length).toLocaleString()}`, '💰', '#3fb950')}
                    ${Components.quickStatCard('Low Stock Items', stats.lowStockCount, `${stats.criticalCount} Critical`, '⚠️', '#d29922')}
                    ${Components.quickStatCard('Warehouses', stats.warehouses, `${stats.suppliers} Suppliers`, '🏢', '#58a6ff')}
                </div>
            `)}
            <div class="charts-grid">
                <div class="chart-box"><div id="chart-stock-status" class="chart-inner"></div></div>
                <div class="chart-box"><div id="chart-category" class="chart-inner"></div></div>
                <div class="chart-box"><div id="chart-warehouse" class="chart-inner"></div></div>
                <div class="chart-box"><div id="chart-top-products" class="chart-inner"></div></div>
            </div>
        `;

        setTimeout(() => {
            ChartRenderer.renderStockStatus('chart-stock-status', stock);
            ChartRenderer.renderCategory('chart-category', stock);
            ChartRenderer.renderWarehouse('chart-warehouse', stock);
            ChartRenderer.renderTopProducts('chart-top-products', stock);
        }, 0);
    }

    calculateStats(stock) {
        return {
            lowStockCount: stock.filter(s => s.Stock_Status === 'Low' || s.Stock_Status === 'Critical').length,
            criticalCount: stock.filter(s => s.Stock_Status === 'Critical').length,
            totalValue: stock.reduce((sum, s) => sum + (parseFloat(s.Total_Value) || 0), 0),
            totalQuantity: stock.reduce((sum, s) => sum + (parseFloat(s.Quantity) || 0), 0),
            warehouses: [...new Set(stock.map(s => s.Warehouse))].length,
            suppliers: [...new Set(stock.map(s => s.Supplier))].length
        };
    }

    // ===== KPI METRICS TAB =====
    renderKPIMetrics(container) {
        const { kpis } = this.data;

        container.innerHTML = `
            ${Components.section('💰 Financial KPIs', `
                <div class="kpi-row">
                    ${Components.kpiCard('inventory_turnover', kpis.inventory_turnover, '🔄', 'Inventory Turnover',
            `${kpis.inventory_turnover?.annual_turnover || 0}x`, kpis.inventory_turnover?.interpretation, '#3fb950')}
                    ${Components.kpiCard('days_sales_inventory', kpis.days_sales_inventory, '📅', 'Days Sales Inventory',
                `${kpis.days_sales_inventory?.dsi || kpis.days_sales_inventory?.days_sales_inventory || 0} days`, kpis.days_sales_inventory?.interpretation, '#58a6ff')}
                    ${Components.kpiCard('carrying_cost', kpis.carrying_cost, '💸', 'Carrying Cost',
                    `$${(kpis.carrying_cost?.annual_carrying_cost || 0).toLocaleString()}`, `${kpis.carrying_cost?.carrying_cost_rate || 0}% rate`, '#d29922')}
                    ${Components.kpiCard('dead_stock_percentage', kpis.dead_stock_percentage, '☠️', 'Dead Stock',
                        `${kpis.dead_stock_percentage?.dead_stock_percentage || 0}%`, `$${(kpis.dead_stock_percentage?.dead_stock_value || 0).toLocaleString()}`, '#f85149')}
                    ${Components.kpiCard('inventory_shrinkage', kpis.inventory_shrinkage, '📉', 'Shrinkage',
                            `${kpis.inventory_shrinkage?.shrinkage_rate || 0}%`, `$${(kpis.inventory_shrinkage?.shrinkage_value || 0).toLocaleString()} loss`, '#f85149')}
                </div>
            `)}
            ${Components.section('⚙️ Operational KPIs', `
                <div class="kpi-row">
                    ${Components.kpiCard('stock_accuracy', kpis.stock_accuracy, '🎯', 'Stock Accuracy',
                                `${kpis.stock_accuracy?.accuracy_rate || 0}%`, `${kpis.stock_accuracy?.accurate_items || 0}/${kpis.stock_accuracy?.total_items || 0} items`, '#3fb950')}
                    ${Components.kpiCard('stockout_rate', kpis.stockout_rate, '⚠️', 'Stockout Rate',
                                    `${kpis.stockout_rate?.stockout_rate || 0}%`, `${kpis.stockout_rate?.stockout_items || 0} items affected`, '#f85149')}
                    ${Components.kpiCard('order_fulfillment', kpis.order_fulfillment, '✅', 'Order Fulfillment',
                                        `${kpis.order_fulfillment?.fulfillment_rate || 0}%`, `${kpis.order_fulfillment?.fulfilled_orders || 0}/${kpis.order_fulfillment?.total_orders || 0} orders`, '#3fb950')}
                    ${Components.kpiCard('backorder_rate', kpis.backorder_rate, '📦', 'Backorder Rate',
                                            `${kpis.backorder_rate?.backorder_rate || 0}%`, `${kpis.backorder_rate?.backorders || 0} backorders`, '#d29922')}
                    ${Components.kpiCard('fill_rate', kpis.fill_rate, '📊', 'Fill Rate',
                                                `${kpis.fill_rate?.fill_rate || 0}%`, `${kpis.fill_rate?.items_in_stock || 0}/${kpis.fill_rate?.total_items || 0} in stock`, '#3fb950')}
                </div>
            `)}
            ${Components.section('🚚 Supply Chain KPIs', `
                <div class="kpi-row">
                    ${Components.kpiCard('lead_time', kpis.lead_time, '⏱️', 'Avg Lead Time',
                                                    `${kpis.lead_time?.average_lead_time_days || kpis.lead_time?.average_lead_time || 0} days`,
                                                    `Min: ${kpis.lead_time?.min_lead_time || 0} | Max: ${kpis.lead_time?.max_lead_time || 0}`, '#58a6ff')}
                    <div class="lead-time-suppliers">
                        <h4 style="color: #c9d1d9; margin-bottom: 15px;">Lead Time by Supplier</h4>
                        <div class="supplier-list">${Components.leadTimeSuppliers(kpis.lead_time?.by_supplier)}</div>
                    </div>
                </div>
            `)}
            ${Components.section('💸 Carrying Cost Breakdown', '<div id="chart-carrying-cost" class="chart-full"></div>')}
        `;

        // Add KPI card click handlers
        document.querySelectorAll('.kpi-card').forEach(card => {
            card.addEventListener('click', () => KpiModal.show(card.dataset.kpiId, this.data));
        });

        setTimeout(() => ChartRenderer.renderCarryingCost('chart-carrying-cost', kpis.carrying_cost), 0);
    }

    // ===== ANALYTICS TAB =====
    renderAnalytics(container) {
        const { kpis, transactions } = this.data;
        const abc = kpis.abc_analysis || {};
        const valuation = kpis.inventory_valuation || {};

        container.innerHTML = `
            ${Components.section('📊 ABC Analysis', `
                <div class="abc-grid">
                    ${Components.abcCard('A', abc.category_A, '#f85149', '#3d1f1f')}
                    ${Components.abcCard('B', abc.category_B, '#d29922', '#3d2f1a')}
                    ${Components.abcCard('C', abc.category_C, '#3fb950', '#1f3d23')}
                </div>
            `)}
            ${Components.section('💎 Inventory Valuation Methods', `
                <div class="kpi-row">
                    ${Components.valuationCard('FIFO Method', valuation.fifo_valuation, 'First In First Out', '1️⃣', '#58a6ff')}
                    ${Components.valuationCard('Average Cost', valuation.average_cost_valuation, 'Simple Average', '2️⃣', '#58a6ff')}
                    ${Components.valuationCard('Weighted Avg', valuation.weighted_average_valuation, 'Quantity Weighted', '3️⃣', '#3fb950')}
                    ${Components.valuationCard('Total Units', valuation.total_units, 'All Warehouses', '📦', '#d29922', false)}
                </div>
            `)}
            ${Components.section('🏆 Supplier Performance', '<div id="chart-supplier-performance" class="chart-full"></div>')}
            ${Components.section('⏳ Item Aging Analysis', `
                <div class="charts-grid">
                    <div class="chart-box"><div id="chart-aging-count" class="chart-inner"></div></div>
                    <div class="chart-box"><div id="chart-aging-value" class="chart-inner"></div></div>
                </div>
            `)}
            ${Components.section('📈 Transaction Trends', '<div id="chart-trends" class="chart-full"></div>')}
        `;

        setTimeout(() => {
            ChartRenderer.renderSupplierPerformance('chart-supplier-performance', kpis.supplier_performance);
            ChartRenderer.renderAging('chart-aging-count', 'chart-aging-value', kpis.item_aging);
            ChartRenderer.renderTrends('chart-trends', transactions);
        }, 0);
    }

    // ===== DETAILS TAB =====
    renderDetails(container) {
        const { stock } = this.data;
        const warehouses = [...new Set(stock.map(s => s.Warehouse))];

        container.innerHTML = `
            ${Components.section('📋 Detailed Stock Inventory', `
                <div class="table-controls">
                    <input type="text" id="table-search" placeholder="🔍 Search products..." class="table-search">
                    <select id="status-filter" class="table-filter">
                        <option value="">All Status</option>
                        <option value="Critical">Critical</option>
                        <option value="Low">Low</option>
                        <option value="Adequate">Adequate</option>
                        <option value="Overstocked">Overstocked</option>
                    </select>
                    <select id="warehouse-filter" class="table-filter">
                        <option value="">All Warehouses</option>
                        ${warehouses.map(w => `<option value="${w}">${w}</option>`).join('')}
                    </select>
                    <button id="export-btn" class="export-btn">📥 Export CSV</button>
                </div>
                <div class="table-wrapper">
                    <table id="stock-table" class="data-table">
                        <thead>
                            <tr>
                                <th data-sort="SKU">SKU ↕</th>
                                <th data-sort="Product">Product ↕</th>
                                <th data-sort="Category">Category ↕</th>
                                <th data-sort="Quantity">Quantity ↕</th>
                                <th data-sort="Reorder_Level">Reorder ↕</th>
                                <th data-sort="Unit_Price">Unit Price ↕</th>
                                <th data-sort="Total_Value">Total Value ↕</th>
                                <th data-sort="Stock_Status">Status ↕</th>
                                <th data-sort="Warehouse">Warehouse ↕</th>
                                <th data-sort="Supplier">Supplier ↕</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">${DataTable.renderRows(stock)}</tbody>
                    </table>
                </div>
                <p class="table-info">Showing ${stock.length} products</p>
            `)}
        `;

        DataTable.setupInteractions(stock, 'table-body', '.table-info');
    }

    // ===== FORECASTING TAB =====
    renderForecasting(container) {
        const { stock } = this.data;
        const products = stock.map(s => ({ id: s.SKU || s.Product_ID, name: s.Product }));

        container.innerHTML = `
            ${Components.section('🔮 Demand Forecasting', `
                <div class="forecast-controls">
                    <div class="control-group">
                        <label for="forecast-product">Select Product:</label>
                        <select id="forecast-product" class="table-filter">
                            <option value="">All Products (Aggregate)</option>
                            ${products.map(p => `<option value="${p.id}">${p.name}</option>`).join('')}
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="forecast-periods">Forecast Period:</label>
                        <select id="forecast-periods" class="table-filter">
                            <option value="7">7 Days</option>
                            <option value="14">14 Days</option>
                            <option value="30" selected>30 Days</option>
                            <option value="60">60 Days</option>
                            <option value="90">90 Days</option>
                        </select>
                    </div>
                    <div class="control-group">
                        <label for="forecast-model">Model:</label>
                        <select id="forecast-model" class="table-filter">
                            <option value="auto">Auto Select</option>
                            <option value="simple">Simple Moving Avg</option>
                            <option value="xgboost">XGBoost</option>
                            <option value="prophet">Prophet</option>
                        </select>
                    </div>
                    <button id="generate-forecast" class="export-btn">🔮 Generate Forecast</button>
                </div>
            `)}
            
            <div id="forecast-results" class="section-container" style="display: none;">
                <h3 class="section-header">📈 Forecast Results</h3>
                <div id="forecast-chart" class="chart-full"></div>
                <div id="forecast-metrics" class="kpi-row" style="margin-top: 20px;"></div>
            </div>

            <div id="forecast-table-section" class="section-container" style="display: none;">
                <h3 class="section-header">📊 Forecast Data</h3>
                <div class="table-wrapper">
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Forecast</th>
                                <th>Lower Bound</th>
                                <th>Upper Bound</th>
                            </tr>
                        </thead>
                        <tbody id="forecast-table-body"></tbody>
                    </table>
                </div>
            </div>

            ${Components.section('💡 About Forecasting', `
                <div class="info-grid">
                    <div class="info-card">
                        <h4>🤖 Auto Model</h4>
                        <p>Automatically selects the best model based on your data size and patterns.</p>
                    </div>
                    <div class="info-card">
                        <h4>📊 Simple Moving Average</h4>
                        <p>Fast, works with any data size. Best for stable demand patterns.</p>
                    </div>
                    <div class="info-card">
                        <h4>🚀 XGBoost</h4>
                        <p>Machine learning model. Excellent for medium datasets with trends.</p>
                    </div>
                    <div class="info-card">
                        <h4>📈 Prophet</h4>
                        <p>Facebook's model for seasonality. Best for daily data with holidays.</p>
                    </div>
                </div>
            `)}
        `;

        // Setup event listener
        document.getElementById('generate-forecast')?.addEventListener('click', () => this.generateForecast());
    }

    async generateForecast() {
        const productId = document.getElementById('forecast-product').value;
        const periods = parseInt(document.getElementById('forecast-periods').value);
        const model = document.getElementById('forecast-model').value;

        const btn = document.getElementById('generate-forecast');
        btn.disabled = true;
        btn.innerHTML = '⏳ Generating...';

        try {
            const response = await fetch('/api/forecast/demand', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ product_id: productId || null, periods, model })
            });

            const result = await response.json();

            if (result.success) {
                this.displayForecast(result.data);
            } else {
                alert('Forecast failed: ' + result.error);
            }
        } catch (error) {
            console.error('Forecast error:', error);
            alert('Failed to generate forecast. Check console for details.');
        } finally {
            btn.disabled = false;
            btn.innerHTML = '🔮 Generate Forecast';
        }
    }

    displayForecast(data) {
        // Show results section
        document.getElementById('forecast-results').style.display = 'block';
        document.getElementById('forecast-table-section').style.display = 'block';

        const forecast = data.forecast;
        const dates = forecast.map(f => f.date);
        const values = forecast.map(f => f.forecast);
        const lowerBounds = forecast.map(f => f.lower_bound);
        const upperBounds = forecast.map(f => f.upper_bound);

        // Render chart
        Plotly.newPlot('forecast-chart', [
            {
                name: 'Forecast',
                x: dates,
                y: values,
                type: 'scatter',
                mode: 'lines+markers',
                line: { color: '#58a6ff', width: 3 },
                marker: { size: 8 }
            },
            {
                name: 'Upper Bound',
                x: dates,
                y: upperBounds,
                type: 'scatter',
                mode: 'lines',
                line: { color: '#3fb950', dash: 'dash', width: 1 },
                fill: 'none'
            },
            {
                name: 'Lower Bound',
                x: dates,
                y: lowerBounds,
                type: 'scatter',
                mode: 'lines',
                line: { color: '#f85149', dash: 'dash', width: 1 },
                fill: 'tonexty',
                fillcolor: 'rgba(88, 166, 255, 0.1)'
            }
        ], {
            title: `Demand Forecast (${data.model})`,
            paper_bgcolor: '#161b22',
            plot_bgcolor: '#161b22',
            font: { color: '#c9d1d9' },
            height: 400,
            legend: { x: 0.01, y: 0.99 },
            xaxis: { title: 'Date' },
            yaxis: { title: 'Predicted Demand' }
        }, { responsive: true });

        // Render metrics
        const totalDemand = values.reduce((a, b) => a + b, 0);
        const avgDemand = totalDemand / values.length;
        const maxDemand = Math.max(...values);
        const minDemand = Math.min(...values);

        document.getElementById('forecast-metrics').innerHTML = `
            ${Components.quickStatCard('Total Demand', Math.round(totalDemand), `${data.periods} days`, '📦', '#58a6ff')}
            ${Components.quickStatCard('Avg Daily', Math.round(avgDemand), 'units/day', '📊', '#3fb950')}
            ${Components.quickStatCard('Peak Demand', Math.round(maxDemand), 'max units', '📈', '#d29922')}
            ${Components.quickStatCard('Model Used', data.model, data.metrics?.mape ? `MAPE: ${data.metrics.mape}%` : '', '🤖', '#58a6ff')}
        `;

        // Render table
        document.getElementById('forecast-table-body').innerHTML = forecast.map(f => `
            <tr>
                <td>${f.date.split('T')[0]}</td>
                <td>${Math.round(f.forecast)}</td>
                <td>${Math.round(f.lower_bound)}</td>
                <td>${Math.round(f.upper_bound)}</td>
            </tr>
        `).join('');
    }

    // ===== UTILITIES =====
    showLoading(show) {
        const loading = document.getElementById('loading');
        if (loading) loading.style.display = show ? 'flex' : 'none';
    }

    showError(message) {
        const container = document.getElementById('tab-content');
        if (container) {
            container.innerHTML = `
                <div style="padding: 40px; text-align: center;">
                    <h2 style="color: #f85149;">❌ Error</h2>
                    <p style="color: #8b949e;">${message}</p>
                    <button onclick="location.reload()" class="reload-btn">Reload Dashboard</button>
                </div>
            `;
        }
    }

    updateLastUpdated(timestamp) {
        const el = document.getElementById('update-time');
        if (el) el.textContent = timestamp;
    }
}

// Initialize app
let app;
document.addEventListener('DOMContentLoaded', () => {
    app = new StockDashboardApp();
    window.app = app;
});
