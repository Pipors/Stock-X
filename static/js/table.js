// Data Table Module - Table rendering, filtering, sorting, export
// static/js/table.js

const DataTable = {
  // Render table rows
  renderRows(data) {
    return data.map(row => {
      const statusClass = row.Stock_Status === 'Critical' ? 'status-critical' :
        row.Stock_Status === 'Low' ? 'status-low' :
          row.Stock_Status === 'Overstocked' ? 'status-overstocked' : '';
      return `
                <tr class="${statusClass}">
                    <td>${row.SKU || '-'}</td>
                    <td>${row.Product || '-'}</td>
                    <td>${row.Category || '-'}</td>
                    <td>${row.Quantity || 0}</td>
                    <td>${row.Reorder_Level || 0}</td>
                    <td>$${(row.Unit_Price || 0).toFixed(2)}</td>
                    <td>$${(row.Total_Value || 0).toLocaleString()}</td>
                    <td><span class="status-badge ${statusClass}">${row.Stock_Status || '-'}</span></td>
                    <td>${row.Warehouse || '-'}</td>
                    <td>${row.Supplier || '-'}</td>
                </tr>
            `;
    }).join('');
  },

  // Setup table interactions (filter, sort, export)
  setupInteractions(stock, tbodyId, infoSelector) {
    const search = document.getElementById('table-search');
    const statusFilter = document.getElementById('status-filter');
    const warehouseFilter = document.getElementById('warehouse-filter');
    const exportBtn = document.getElementById('export-btn');
    const tbody = document.getElementById(tbodyId);

    const filterTable = () => {
      const searchTerm = search?.value.toLowerCase() || '';
      const statusVal = statusFilter?.value || '';
      const warehouseVal = warehouseFilter?.value || '';

      const filtered = stock.filter(row => {
        const matchSearch = !searchTerm ||
          row.Product?.toLowerCase().includes(searchTerm) ||
          row.SKU?.toLowerCase().includes(searchTerm) ||
          row.Category?.toLowerCase().includes(searchTerm);
        const matchStatus = !statusVal || row.Stock_Status === statusVal;
        const matchWarehouse = !warehouseVal || row.Warehouse === warehouseVal;
        return matchSearch && matchStatus && matchWarehouse;
      });

      tbody.innerHTML = this.renderRows(filtered);
      const infoEl = document.querySelector(infoSelector);
      if (infoEl) infoEl.textContent = `Showing ${filtered.length} of ${stock.length} products`;
    };

    search?.addEventListener('input', filterTable);
    statusFilter?.addEventListener('change', filterTable);
    warehouseFilter?.addEventListener('change', filterTable);

    // Sorting
    document.querySelectorAll('th[data-sort]').forEach(th => {
      th.addEventListener('click', () => {
        const field = th.dataset.sort;
        const sorted = [...stock].sort((a, b) => {
          const aVal = a[field] || '';
          const bVal = b[field] || '';
          return aVal > bVal ? 1 : -1;
        });
        tbody.innerHTML = this.renderRows(sorted);
      });
    });

    // Export
    exportBtn?.addEventListener('click', () => this.exportToCSV(stock));
  },

  // Export to CSV
  exportToCSV(data) {
    const headers = ['SKU', 'Product', 'Category', 'Quantity', 'Reorder_Level', 'Unit_Price', 'Total_Value', 'Stock_Status', 'Warehouse', 'Supplier'];
    const csv = [headers.join(',')];
    data.forEach(row => {
      csv.push(headers.map(h => `"${row[h] || ''}"`).join(','));
    });
    const blob = new Blob([csv.join('\n')], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `inventory_export_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  }
};

window.DataTable = DataTable;
