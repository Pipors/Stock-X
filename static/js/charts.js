// Chart Rendering Module - All Plotly chart functions
// static/js/charts.js

const ChartRenderer = {
  colors: {
    primary: '#58a6ff',
    success: '#3fb950',
    warning: '#d29922',
    danger: '#f85149',
    muted: '#8b949e',
    background: '#161b22',
    text: '#c9d1d9'
  },

  defaultLayout: {
    paper_bgcolor: '#161b22',
    plot_bgcolor: '#161b22',
    font: { color: '#c9d1d9' },
    height: 400
  },

  // Stock Overview Charts
  renderStockStatus(elementId, stock) {
    const statusCounts = {};
    stock.forEach(item => {
      statusCounts[item.Stock_Status || 'Unknown'] = (statusCounts[item.Stock_Status] || 0) + 1;
    });

    const colorMap = {
      'Overstocked': this.colors.success,
      'Adequate': this.colors.primary,
      'Low': this.colors.warning,
      'Critical': this.colors.danger
    };

    Plotly.newPlot(elementId, [{
      values: Object.values(statusCounts),
      labels: Object.keys(statusCounts),
      type: 'pie',
      hole: 0.4,
      marker: { colors: Object.keys(statusCounts).map(s => colorMap[s] || this.colors.muted) }
    }], {
      ...this.defaultLayout,
      title: 'Stock Status Distribution'
    }, { responsive: true });
  },

  renderCategory(elementId, stock) {
    const catTotals = {};
    stock.forEach(item => {
      catTotals[item.Category || 'Unknown'] = (catTotals[item.Category] || 0) + (parseFloat(item.Quantity) || 0);
    });

    Plotly.newPlot(elementId, [{
      x: Object.keys(catTotals),
      y: Object.values(catTotals),
      type: 'bar',
      marker: { color: this.colors.primary }
    }], {
      ...this.defaultLayout,
      title: 'Stock Quantity by Category'
    }, { responsive: true });
  },

  renderWarehouse(elementId, stock) {
    const whTotals = {};
    stock.forEach(item => {
      whTotals[item.Warehouse || 'Unknown'] = (whTotals[item.Warehouse] || 0) + (parseFloat(item.Total_Value) || 0);
    });

    Plotly.newPlot(elementId, [{
      x: Object.keys(whTotals),
      y: Object.values(whTotals),
      type: 'bar',
      marker: { color: this.colors.success }
    }], {
      ...this.defaultLayout,
      title: 'Stock Value by Warehouse'
    }, { responsive: true });
  },

  renderTopProducts(elementId, stock) {
    const sorted = [...stock].sort((a, b) => (b.Total_Value || 0) - (a.Total_Value || 0)).slice(0, 10);

    Plotly.newPlot(elementId, [{
      y: sorted.map(p => p.Product),
      x: sorted.map(p => p.Total_Value),
      type: 'bar',
      orientation: 'h',
      marker: { color: this.colors.warning }
    }], {
      ...this.defaultLayout,
      title: 'Top 10 Products by Value',
      margin: { l: 150 }
    }, { responsive: true });
  },

  // KPI Charts
  renderCarryingCost(elementId, carrying) {
    if (!carrying?.breakdown) return;
    const breakdown = carrying.breakdown;

    Plotly.newPlot(elementId, [{
      x: Object.keys(breakdown),
      y: Object.values(breakdown),
      type: 'bar',
      marker: { color: [this.colors.primary, this.colors.success, this.colors.warning, this.colors.danger] },
      text: Object.values(breakdown).map(v => `$${v.toLocaleString()}`),
      textposition: 'auto'
    }], {
      ...this.defaultLayout,
      title: 'Carrying Cost Components'
    }, { responsive: true });
  },

  // Analytics Charts
  renderSupplierPerformance(elementId, supplierPerf) {
    if (!supplierPerf?.suppliers) {
      document.getElementById(elementId).innerHTML = '<div style="padding:40px;text-align:center;color:#8b949e">No supplier performance data available</div>';
      return;
    }

    const suppliers = Object.keys(supplierPerf.suppliers);
    const scores = suppliers.map(s => supplierPerf.suppliers[s].quality_score || 0);
    const values = suppliers.map(s => supplierPerf.suppliers[s].total_value || 0);

    Plotly.newPlot(elementId, [
      { name: 'Quality Score', x: suppliers, y: scores, type: 'bar', marker: { color: this.colors.success } },
      { name: 'Total Value', x: suppliers, y: values, type: 'scatter', mode: 'lines+markers', yaxis: 'y2', marker: { color: this.colors.primary, size: 10 } }
    ], {
      ...this.defaultLayout,
      title: 'Supplier Performance Analysis',
      yaxis: { title: 'Quality Score' },
      yaxis2: { title: 'Total Value ($)', overlaying: 'y', side: 'right' },
      legend: { x: 0.01, y: 0.99 }
    }, { responsive: true });
  },

  renderAging(countElementId, valueElementId, aging) {
    if (!aging) {
      document.getElementById(countElementId).innerHTML = '<div style="padding:40px;text-align:center;color:#8b949e">No aging data</div>';
      document.getElementById(valueElementId).innerHTML = '<div style="padding:40px;text-align:center;color:#8b949e">No aging data</div>';
      return;
    }

    const colors = [this.colors.success, this.colors.primary, this.colors.warning, this.colors.danger];

    if (aging.age_distribution) {
      Plotly.newPlot(countElementId, [{
        x: Object.keys(aging.age_distribution),
        y: Object.values(aging.age_distribution),
        type: 'bar',
        marker: { color: colors },
        text: Object.values(aging.age_distribution),
        textposition: 'auto'
      }], { ...this.defaultLayout, title: 'Item Count by Age' }, { responsive: true });
    }

    if (aging.value_by_age) {
      Plotly.newPlot(valueElementId, [{
        x: Object.keys(aging.value_by_age),
        y: Object.values(aging.value_by_age),
        type: 'bar',
        marker: { color: colors },
        text: Object.values(aging.value_by_age).map(v => `$${v.toLocaleString()}`),
        textposition: 'auto'
      }], { ...this.defaultLayout, title: 'Inventory Value by Age' }, { responsive: true });
    }
  },

  renderTrends(elementId, transactions) {
    const dates = {};
    transactions.forEach(t => {
      const date = t.Date?.split('T')[0] || t.Date?.split(' ')[0] || 'Unknown';
      dates[date] = (dates[date] || 0) + (parseFloat(t.Total_Value) || 0);
    });

    const sortedDates = Object.keys(dates).sort();
    Plotly.newPlot(elementId, [{
      x: sortedDates,
      y: sortedDates.map(d => dates[d]),
      type: 'scatter',
      mode: 'lines+markers',
      marker: { color: this.colors.primary },
      line: { color: this.colors.primary, width: 2 }
    }], {
      ...this.defaultLayout,
      title: 'Transaction Value Trends'
    }, { responsive: true });
  }
};

window.ChartRenderer = ChartRenderer;
