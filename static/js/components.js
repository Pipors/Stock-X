// UI Components Module - Reusable HTML generators
// static/js/components.js

const Components = {
  // Quick stat card for overview
  quickStatCard(title, value, subtitle, icon, color) {
    return `
            <div class="quick-stat-card">
                <div class="stat-icon">${icon}</div>
                <h4 class="stat-title">${title}</h4>
                <h2 class="stat-value" style="color: ${color}">${value}</h2>
                <p class="stat-subtitle">${subtitle}</p>
            </div>
        `;
  },

  // KPI card with click handler
  kpiCard(kpiId, kpiData, icon, title, value, subtitle, color) {
    const status = kpiData?.status || '';
    const statusColor = status === 'Excellent' || status === 'Good' ? '#3fb950' :
      status === 'Average' ? '#d29922' : '#8b949e';
    return `
            <div class="kpi-card" data-kpi-id="${kpiId}" style="border-left: 4px solid ${color}">
                <div class="kpi-icon">${icon}</div>
                <h4 class="kpi-title">${title}</h4>
                <h2 class="kpi-value" style="color: ${color}">${value}</h2>
                <p class="kpi-subtitle">${subtitle}</p>
                ${status ? `<span class="kpi-status" style="background-color: ${statusColor}">${status}</span>` : ''}
                <p class="kpi-hint">🔍 Click for details</p>
            </div>
        `;
  },

  // ABC analysis card
  abcCard(letter, data, color, bgColor) {
    if (!data) {
      return `<div class="abc-card" style="background: ${bgColor}; border: 2px solid ${color}"><h2 style="color: ${color}">${letter}</h2><p>No data</p></div>`;
    }
    return `
            <div class="abc-card" style="background: ${bgColor}; border: 2px solid ${color}">
                <h2 class="abc-letter" style="color: ${color}">${letter}</h2>
                <h4 class="abc-count">${data.count || 0} items</h4>
                <p class="abc-percent">${data.percentage || 0}% of items</p>
                <h3 class="abc-value" style="color: ${color}">$${(data.value || 0).toLocaleString()}</h3>
                <p class="abc-value-percent">${data.value_percentage || 0}% of value</p>
            </div>
        `;
  },

  // Valuation method card
  valuationCard(title, value, subtitle, icon, color, isCurrency = true) {
    const displayValue = isCurrency ? `$${(value || 0).toLocaleString()}` : (value || 0).toLocaleString();
    return `
            <div class="valuation-card">
                <div class="val-icon">${icon}</div>
                <h4 class="val-title">${title}</h4>
                <h2 class="val-value" style="color: ${color}">${displayValue}</h2>
                <p class="val-subtitle">${subtitle}</p>
            </div>
        `;
  },

  // Lead time supplier list
  leadTimeSuppliers(bySupplier) {
    const suppliers = Object.entries(bySupplier || {});
    if (suppliers.length === 0) return '<p style="color: #8b949e;">No supplier data</p>';
    return suppliers.map(([supplier, days]) => `
            <div class="supplier-item">
                <span class="supplier-name">${supplier}:</span>
                <span class="supplier-days">${days} days</span>
            </div>
        `).join('');
  },

  // Section container
  section(header, content) {
    return `
            <div class="section-container">
                <h3 class="section-header">${header}</h3>
                ${content}
            </div>
        `;
  }
};

window.Components = Components;
