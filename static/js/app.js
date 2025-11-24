// JavaScript for Inventory Management System

let currentProductId = null;

// Load sales history on dashboard
document.addEventListener('DOMContentLoaded', function() {
    if (document.getElementById('sales-history')) {
        loadSalesHistory();
    }
});

function purchaseProduct(productId) {
    currentProductId = productId;
    
    // Find product details from table
    const row = document.querySelector(`tr td:first-child`);
    const productRow = Array.from(document.querySelectorAll('tbody tr')).find(row => 
        row.cells[0].textContent == productId
    );
    
    if (productRow) {
        document.getElementById('productId').value = productId;
        document.getElementById('productName').value = productRow.cells[1].textContent;
        document.getElementById('quantity').value = 1;
        
        const modal = new bootstrap.Modal(document.getElementById('purchaseModal'));
        modal.show();
    }
}

function confirmPurchase() {
    const productId = document.getElementById('productId').value;
    const quantity = parseInt(document.getElementById('quantity').value);
    
    if (!quantity || quantity < 1) {
        alert('Please enter a valid quantity');
        return;
    }
    
    fetch('/api/purchase', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: parseInt(productId),
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Purchase successful!');
            location.reload(); // Refresh to update stock
        } else {
            alert('Purchase failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred');
    });
    
    // Close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('purchaseModal'));
    modal.hide();
}

function loadSalesHistory() {
    fetch('/api/sales')
    .then(response => response.json())
    .then(sales => {
        const container = document.getElementById('sales-history');
        
        if (sales.length === 0) {
            container.innerHTML = '<p class="text-muted">No sales history</p>';
            return;
        }
        
        let html = '<div class="list-group">';
        sales.slice(-5).reverse().forEach(sale => {
            const date = new Date(sale.sale_date).toLocaleDateString();
            html += `
                <div class="list-group-item">
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1">${sale.product}</h6>
                        <small>${date}</small>
                    </div>
                    <p class="mb-1">Qty: ${sale.quantity} × $${sale.unit_price}</p>
                    <small>Total: $${sale.total_amount}</small>
                </div>
            `;
        });
        html += '</div>';
        
        container.innerHTML = html;
    })
    .catch(error => {
        console.error('Error loading sales:', error);
        document.getElementById('sales-history').innerHTML = 
            '<p class="text-danger">Error loading sales history</p>';
    });
}

// Admin functions
function addProduct() {
    const name = prompt('Product Name:');
    const price = parseFloat(prompt('Price:'));
    const quantity = parseInt(prompt('Quantity:'));
    const category = prompt('Category (optional):');
    
    if (!name || !price || !quantity) {
        alert('Please provide valid product details');
        return;
    }
    
    fetch('/api/admin/products', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            price: price,
            quantity: quantity,
            category: category
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product added successfully!');
            location.reload();
        } else {
            alert('Failed to add product: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred');
    });
}