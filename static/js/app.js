// InvenTrack — Premium UI JavaScript

let currentProductId = null;

document.addEventListener('DOMContentLoaded', function () {
    if (document.getElementById('sales-history')) {
        loadSalesHistory();
    }

    // Close sidebar on outside click (mobile)
    document.addEventListener('click', function (e) {
        const sidebar = document.getElementById('sidebar');
        const toggle = document.querySelector('.sidebar-toggle');
        if (sidebar && sidebar.classList.contains('show') &&
            !sidebar.contains(e.target) && !toggle?.contains(e.target)) {
            sidebar.classList.remove('show');
        }
    });
});

/* ---- Toast Notifications ---- */
function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const icons = {
        success: 'bi-check-circle-fill',
        error: 'bi-x-circle-fill',
        warning: 'bi-exclamation-triangle-fill'
    };

    const id = 'toast-' + Date.now();
    const html = `
        <div id="${id}" class="toast toast-custom toast-${type}" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex align-items-center p-3">
                <i class="bi ${icons[type] || icons.success} me-2" style="font-size:1.1rem;"></i>
                <div class="flex-grow-1" style="font-size:0.875rem; font-weight:500;">${message}</div>
                <button type="button" class="btn-close btn-close-sm ms-2" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    container.insertAdjacentHTML('beforeend', html);

    const toastEl = document.getElementById(id);
    const toast = new bootstrap.Toast(toastEl, { delay: 4000 });
    toast.show();
    toastEl.addEventListener('hidden.bs.toast', () => toastEl.remove());
}

/* ---- Purchase Flow ---- */
function purchaseProduct(productId) {
    currentProductId = productId;
    const productRow = Array.from(document.querySelectorAll('tbody tr')).find(row => {
        const btn = row.querySelector('[data-product-id]');
        return btn && btn.dataset.productId == productId;
    });

    if (productRow) {
        const nameEl = productRow.querySelector('.product-name');
        document.getElementById('productId').value = productId;
        document.getElementById('productName').value = nameEl ? nameEl.textContent.trim() : '';
        document.getElementById('quantity').value = 1;

        const modal = new bootstrap.Modal(document.getElementById('purchaseModal'));
        modal.show();
    }
}

function confirmPurchase() {
    const productId = document.getElementById('productId').value;
    const quantity = parseInt(document.getElementById('quantity').value);

    if (!quantity || quantity < 1) {
        showToast('Please enter a valid quantity', 'warning');
        return;
    }

    const btn = document.querySelector('#purchaseModal .btn-primary');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Processing...';
    btn.disabled = true;

    fetch('/api/purchase', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: parseInt(productId), quantity: quantity })
    })
    .then(res => res.json())
    .then(data => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('purchaseModal'));
        modal.hide();
        if (data.success) {
            showToast('Purchase completed successfully', 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showToast('Purchase failed: ' + data.message, 'error');
        }
    })
    .catch(() => {
        showToast('An error occurred. Please try again.', 'error');
    })
    .finally(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    });
}

/* ---- Sales History ---- */
function loadSalesHistory() {
    fetch('/api/sales')
    .then(res => res.json())
    .then(sales => {
        const container = document.getElementById('sales-history');

        if (sales.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <i class="bi bi-receipt-cutoff"></i>
                    <p>No sales yet</p>
                </div>`;
            return;
        }

        let html = '';
        sales.slice(-5).reverse().forEach(sale => {
            const date = new Date(sale.sale_date).toLocaleDateString('en-US', {
                month: 'short', day: 'numeric'
            });
            html += `
                <div class="sale-item">
                    <div class="sale-item-icon"><i class="bi bi-bag-check"></i></div>
                    <div class="sale-item-details">
                        <div class="sale-item-name">${sale.product}</div>
                        <div class="sale-item-meta">${sale.quantity} × $${Number(sale.unit_price).toFixed(2)} · ${date}</div>
                    </div>
                    <div class="sale-item-amount">$${Number(sale.total_amount).toFixed(2)}</div>
                </div>`;
        });

        container.innerHTML = html;
    })
    .catch(() => {
        document.getElementById('sales-history').innerHTML = `
            <div class="empty-state">
                <i class="bi bi-wifi-off"></i>
                <p>Could not load sales history</p>
            </div>`;
    });
}

/* ---- Admin: Add Product (Modal-based) ---- */
function openAddProductModal() {
    const form = document.getElementById('addProductForm');
    if (form) form.reset();
    const modal = new bootstrap.Modal(document.getElementById('addProductModal'));
    modal.show();
}

function addProduct() {
    const name = document.getElementById('newProductName').value.trim();
    const price = parseFloat(document.getElementById('newProductPrice').value);
    const quantity = parseInt(document.getElementById('newProductQty').value);
    const category = document.getElementById('newProductCategory').value.trim();

    if (!name || isNaN(price) || isNaN(quantity)) {
        showToast('Please fill in all required fields', 'warning');
        return;
    }

    const btn = document.querySelector('#addProductModal .btn-primary');
    const originalText = btn.innerHTML;
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span>Adding...';
    btn.disabled = true;

    fetch('/api/admin/products', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, price, quantity, category: category || null })
    })
    .then(res => res.json())
    .then(data => {
        const modal = bootstrap.Modal.getInstance(document.getElementById('addProductModal'));
        modal.hide();
        if (data.success) {
            showToast('Product added successfully', 'success');
            setTimeout(() => location.reload(), 800);
        } else {
            showToast('Failed: ' + data.message, 'error');
        }
    })
    .catch(() => {
        showToast('An error occurred. Please try again.', 'error');
    })
    .finally(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    });
}
