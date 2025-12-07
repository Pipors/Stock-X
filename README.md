# Stock-X: Advanced Stock Management Dashboard

A comprehensive, real-time inventory management dashboard built with Python Dash and PostgreSQL. This system provides advanced KPI analytics, interactive visualizations, and detailed inventory tracking capabilities for modern warehouse operations.

![Dashboard](https://img.shields.io/badge/Dashboard-Dash-blue)
![Database](https://img.shields.io/badge/Database-PostgreSQL-316192)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python)
![Status](https://img.shields.io/badge/Status-Active-success)

## 🌟 Features

### Core Functionality
- **Real-time Inventory Tracking**: Live stock levels across multiple warehouses
- **11 Comprehensive KPIs**: Clickable KPI cards with detailed calculation breakdowns
- **Advanced Analytics**: ABC analysis, supplier performance metrics, and inventory aging
- **Transaction History**: Complete audit trail of all inventory movements
- **Interactive Visualizations**: Dynamic charts using Plotly for data exploration
- **Multi-warehouse Support**: Track inventory across multiple locations
- **Database Integration**: PostgreSQL backend with optimized queries and views

### Dashboard Tabs
1. **📊 Stock Dashboard** - Real-time inventory overview with key metrics
2. **🎯 KPI Metrics** - 11 interactive KPI cards with detailed drill-down
3. **📊 Advanced Analytics** - ABC classification, supplier analysis, and aging reports
4. **📋 Inventory Details** - Filterable, sortable data tables with full product information

### Key Performance Indicators (KPIs)
- Inventory Turnover Ratio
- Days Sales of Inventory (DSI)
- Stock-out Rate
- Order Fill Rate
- Carrying Cost Percentage
- Inventory Accuracy
- Dead Stock Percentage
- Reorder Point Achievement
- Supplier Lead Time
- Average Inventory Age
- Stock-to-Sales Ratio

## 🛠 Technology Stack

- **Backend**: Python 3.8+
- **Database**: PostgreSQL 12+ (running in Docker container)
- **Web Framework**: Dash 2.14.2
- **Visualization**: Plotly 5.18.0
- **Data Processing**: Pandas 2.1.4, NumPy 1.26.2
- **Database Driver**: psycopg2
- **Environment Management**: python-dotenv

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.8 or higher
- Docker Desktop (for PostgreSQL container)
- pip (Python package manager)
- Git (for cloning the repository)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Pipors/Stock-X.git
cd Stock-X
```

### 2. Set Up Python Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r dashboard_requirements.txt
```

Additional dependencies (if needed):
```bash
pip install psycopg2-binary python-dotenv
```

## 🗄️ Database Setup

### 1. Start PostgreSQL Container

```bash
# Pull and run PostgreSQL in Docker
docker run --name postgres-stock \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=stock_management \
  -p 5432:5432 \
  -d postgres:15
```

**⚠️ Security Note**: The default credentials above (postgres/postgres) are for development only. For production environments, use strong passwords and consider:
- Using Docker secrets or environment files
- Implementing proper access controls
- Enabling SSL/TLS connections
- Regular security audits

### 2. Verify Container is Running

```bash
docker ps | grep postgres-stock
```

### 3. Create Database Schema

```bash
# Copy schema file to container
docker cp database_schema.sql postgres-stock:/tmp/

# Execute schema creation
docker exec -it postgres-stock psql -U postgres -d stock_management -f /tmp/database_schema.sql
```

### 4. Load Sample Data (Optional)

```bash
# Copy sample data file
docker cp sample_data.sql postgres-stock:/tmp/

# Load sample data
docker exec -it postgres-stock psql -U postgres -d stock_management -f /tmp/sample_data.sql
```

### 5. Verify Database Setup

```bash
# Connect to database
docker exec -it postgres-stock psql -U postgres -d stock_management

# List tables
\dt

# Check sample data
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM inventory;

# Exit
\q
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root (optional, defaults are provided):

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=stock_management
DB_USER=postgres
DB_PASSWORD=postgres
```

### Application Configuration

Edit `config.py` to customize:
- Dashboard port (default: 3000)
- Debug mode
- Color scheme
- Theme settings

## 🎯 Usage

### Start the Dashboard

```bash
# Ensure virtual environment is activated
python app.py
```

The dashboard will be available at: `http://127.0.0.1:3000`

### First Time Setup

1. Start PostgreSQL container (see Database Setup)
2. Create schema and load sample data
3. Verify database connection with `python test_connection.py`
4. Start the application with `python app.py`

### Testing Database Connection

```bash
python test_connection.py
```

This will verify:
- PostgreSQL container is running
- Database connection is successful
- Required tables exist
- Sample data is loaded

## 📁 Project Structure

```
Stock-X/
├── app.py                      # Main application entry point
├── config.py                   # Configuration and color schemes
├── database.py                 # Database connection and queries
├── kpi_calculator.py          # KPI calculation logic
├── charts.py                   # Chart generation with Plotly
├── ui_components.py           # Reusable UI components
├── kpi_modals.py              # KPI detail modal dialogs
├── tab_renderers.py           # Tab content rendering
├── callbacks.py               # Dash callback handlers
├── database_schema.sql        # PostgreSQL schema definition
├── sample_data.sql            # Sample data for testing
├── dashboard_requirements.txt # Python dependencies
├── test_connection.py         # Database connection tester
└── README.md                  # This file
```

## 🎨 Dashboard Components

### Module Breakdown

1. **app.py**: Main orchestrator that initializes and runs the dashboard
2. **database.py**: Handles PostgreSQL connections and data access
3. **kpi_calculator.py**: Calculates all 11 inventory KPIs with detailed formulas
4. **charts.py**: Creates interactive Plotly visualizations
5. **ui_components.py**: Builds reusable UI elements (headers, cards, etc.)
6. **kpi_modals.py**: Generates detailed KPI explanation modals
7. **tab_renderers.py**: Renders content for each dashboard tab
8. **callbacks.py**: Manages interactivity and user actions

## 📊 Database Schema

The system uses a comprehensive PostgreSQL schema with the following main tables:

- **products**: Master product catalog
- **inventory**: Current stock levels per warehouse
- **categories**: Product categorization
- **suppliers**: Supplier information
- **warehouses**: Warehouse/location data
- **transaction_history**: Complete audit trail
- **purchase_orders**: Inbound purchase orders
- **sales_orders**: Outbound sales orders
- **stock_adjustments**: Manual adjustments and corrections
- **product_movements**: Inter-warehouse transfers

### Database Views

Pre-built views for common queries:
- `v_current_stock_summary`: Aggregated stock across all warehouses
- `v_stock_by_warehouse`: Stock levels per warehouse
- `v_recent_transactions`: Transaction history
- `v_expiring_products`: Products nearing expiry
- `v_low_stock_alert`: Items below reorder point

## 🔍 Key Features Detail

### Interactive KPI Cards

Each KPI card is clickable and displays:
- Current metric value
- Trend indicator (↑/↓)
- Visual status indicator
- Detailed calculation breakdown modal
- Data source and formula explanation

### Advanced Analytics

- **ABC Analysis**: Classify inventory by value contribution
- **Supplier Performance**: Track lead times and reliability
- **Inventory Aging**: Identify slow-moving stock
- **Stock Velocity**: Fast, medium, and slow movers

### Real-time Updates

All data is fetched directly from PostgreSQL, ensuring:
- No cached or stale data
- Real-time inventory accuracy
- Immediate reflection of database changes

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check if container is running
docker ps | grep postgres-stock

# Check container logs
docker logs postgres-stock

# Verify port mapping
docker port postgres-stock

# Restart container
docker restart postgres-stock
```

### Common Issues

1. **Container not running**: Start with `docker start postgres-stock`
2. **Port already in use**: Change port in docker run command or config
3. **Permission denied**: Ensure Docker is running with proper privileges
4. **Module not found**: Reinstall dependencies with `pip install -r dashboard_requirements.txt`

### Database Access

```bash
# Direct database access
docker exec -it postgres-stock psql -U postgres -d stock_management

# Check active connections
SELECT * FROM pg_stat_activity;

# View table sizes (formatted for safety)
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(quote_ident(schemaname)||'.'||quote_ident(tablename))) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(quote_ident(schemaname)||'.'||quote_ident(tablename)) DESC;
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is available for educational and commercial use. Please check the repository for specific license terms.

## 👤 Author

**Pipors**
- GitHub: [@Pipors](https://github.com/Pipors)
- Repository: [Stock-X](https://github.com/Pipors/Stock-X)

## 🙏 Acknowledgments

- Built with [Dash](https://dash.plotly.com/) by Plotly
- Database: PostgreSQL
- Visualizations: Plotly
- UI Design: Custom dark theme optimized for readability

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the troubleshooting section

---

**Note**: This dashboard is designed for inventory management and warehouse operations. Ensure you have proper database backups and security measures in place for production use.
