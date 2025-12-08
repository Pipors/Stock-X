// KPI Modal Module - Modal display and content generation
// static/js/modal.js

const KpiModal = {
  // Show modal with KPI details
  async show(kpiId, data) {
    try {
      const kpiData = await ApiService.getKpiDetails(kpiId);
      const modal = document.getElementById('kpi-modal');
      const content = document.getElementById('kpi-modal-content');

      content.innerHTML = `
                <div class="modal-card">
                    <div class="modal-header">
                        <h2>${kpiData.title || kpiId}</h2>
                        <button onclick="KpiModal.close()" class="modal-close">×</button>
                    </div>
                    
                    <div class="modal-value-box">
                        <div class="modal-big-value">${this.formatValue(kpiId, kpiData)}</div>
                        <p class="modal-subtitle">${kpiData.subtitle || kpiData.interpretation || ''}</p>
                    </div>

                    ${kpiData.formula ? `
                        <div class="modal-section">
                            <h4 class="section-title" style="color: #58a6ff">📐 Formula</h4>
                            <p class="formula-text">${kpiData.formula}</p>
                        </div>
                    ` : ''}

                    ${this.renderCalculationSteps(kpiId, kpiData, data)}

                    ${kpiData.interpretation ? `
                        <div class="modal-section">
                            <h4 class="section-title" style="color: #3fb950">💡 Interpretation</h4>
                            <p>${kpiData.interpretation}</p>
                        </div>
                    ` : ''}

                    ${kpiData.benchmark ? `
                        <div class="modal-section benchmark">
                            <h4 class="section-title" style="color: #d29922">🎯 Benchmark</h4>
                            <p>${kpiData.benchmark}</p>
                        </div>
                    ` : ''}

                    ${this.renderRelatedProducts(kpiId, data?.stock || [])}
                </div>
            `;

      modal.classList.add('show');
    } catch (error) {
      console.error('Failed to load KPI:', error);
    }
  },

  // Close modal
  close() {
    document.getElementById('kpi-modal')?.classList.remove('show');
  },

  // Format KPI value based on type
  formatValue(kpiId, kpiData) {
    if (kpiId.includes('rate') || kpiId.includes('percentage') || kpiId.includes('accuracy')) {
      return `${kpiData.value || kpiData[kpiId] || 0}%`;
    }
    if (kpiId.includes('cost') || kpiId.includes('value') || kpiId.includes('shrinkage')) {
      return `$${(kpiData.value || kpiData.annual_carrying_cost || 0).toLocaleString()}`;
    }
    if (kpiId.includes('turnover')) {
      return `${kpiData.annual_turnover || kpiData.value || 0}x`;
    }
    if (kpiId.includes('days') || kpiId.includes('lead_time')) {
      return `${kpiData.dsi || kpiData.days_sales_inventory || kpiData.average_lead_time_days || 0} days`;
    }
    return kpiData.value || 'N/A';
  },

  // Render calculation steps
  renderCalculationSteps(kpiId, kpiData, data) {
    const stock = data?.stock || [];
    const totalValue = stock.reduce((sum, s) => sum + (parseFloat(s.Total_Value) || 0), 0);
    const totalItems = stock.length;

    const stepsMap = {
      'inventory_turnover': [
        `1. Total Inventory Value: $${totalValue.toLocaleString()}`,
        `2. Number of Products: ${totalItems}`,
        `3. Estimated COGS (60%): $${(totalValue * 0.6).toLocaleString()}`,
        `4. Annual Turnover: ${kpiData.annual_turnover || 0}x`
      ],
      'stockout_rate': [
        `1. Total Items: ${totalItems}`,
        `2. Items Below Reorder: ${kpiData.stockout_items || 0}`,
        `3. Stockout Rate: ${kpiData.stockout_rate || 0}%`
      ],
      'carrying_cost': [
        `1. Inventory Value: $${totalValue.toLocaleString()}`,
        `2. Carrying Rate: ${kpiData.carrying_cost_rate || 25}%`,
        `3. Annual Cost: $${(kpiData.annual_carrying_cost || 0).toLocaleString()}`
      ]
    };

    const steps = stepsMap[kpiId];
    if (!steps) return '';

    return `
            <div class="modal-section calculation-steps">
                <h4 class="section-title" style="color: #58a6ff">🔢 Calculation Steps</h4>
                ${steps.map(step => `<p class="calc-step">${step}</p>`).join('')}
            </div>
        `;
  },

  // Render related products table
  renderRelatedProducts(kpiId, stock) {
    let products = [];

    if (kpiId === 'stockout_rate' || kpiId === 'backorder_rate') {
      products = stock.filter(s => s.Stock_Status === 'Critical' || s.Stock_Status === 'Low').slice(0, 5);
    } else if (kpiId === 'dead_stock_percentage') {
      products = stock.filter(s => s.Stock_Status === 'Overstocked').slice(0, 5);
    } else {
      products = [...stock].sort((a, b) => (b.Total_Value || 0) - (a.Total_Value || 0)).slice(0, 5);
    }

    if (products.length === 0) return '';

    return `
            <div class="modal-section">
                <h4 class="section-title" style="color: #58a6ff">📦 Related Products</h4>
                <table class="modal-table">
                    <thead><tr><th>Product</th><th>Qty</th><th>Value</th><th>Status</th></tr></thead>
                    <tbody>
                        ${products.map(p => `
                            <tr>
                                <td>${p.Product}</td>
                                <td>${p.Quantity}</td>
                                <td>$${(p.Total_Value || 0).toLocaleString()}</td>
                                <td>${p.Stock_Status}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
  }
};

window.KpiModal = KpiModal;
