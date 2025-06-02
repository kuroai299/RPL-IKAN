// Sample product data (can be fetched from Django backend)
const products = {
    Fish: [
        { name: 'Goldfish', price: 20000, stock: 50, id: 1 },
        { name: 'Betta', price: 25000, stock: 30, id: 2 }
    ],
    FishMedicine: [
        { name: 'Herbal Medicine', price: 50000, stock: 10, id: 3 }
    ],
    AquariumStuff: [
        { name: 'Water Filter', price: 150000, stock: 5, id: 4 }
    ],
    FishFood: [
        { name: 'Fish Flakes', price: 20000, stock: 100, id: 5 }
    ]
};

let editingProductId = null; // Track the product being edited

// Function to update the product list based on the selected category
function updateProductList(category) {
    const productList = products[category];
    const productContainer = document.getElementById('productList');
    productContainer.innerHTML = ''; // Clear previous products

    productList.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.classList.add('col-md-3', 'mb-4');
        productDiv.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">Price: ${product.price}</p>
                    <p class="card-text">Stock: ${product.stock}</p>
                    <button class="btn btn-warning btn-sm" onclick="editProduct(${product.id})">Edit</button>
                </div>
            </div>
        `;
        productContainer.appendChild(productDiv);
    });
}

// Function to show the modal for adding a new product
function showAddProductModal() {
    $('#productModalLabel').text('Add Product');
    $('#productName').val('');
    $('#productPrice').val('');
    $('#productStock').val('');
    $('#deleteProductButton').hide(); // Hide delete button when adding a product
    editingProductId = null; // Reset the editing product
    $('#productModal').modal('show');
}

// Function to display the modal for editing an existing product
function editProduct(id) {
    const category = getCategoryFromActiveButton();
    const product = products[category].find(p => p.id === id);

    $('#productModalLabel').text('Edit Product');
    $('#productName').val(product.name);
    $('#productPrice').val(product.price);
    $('#productStock').val(product.stock);
    $('#deleteProductButton').show(); // Show delete button in edit mode
    editingProductId = id; // Set the product ID being edited
    $('#productModal').modal('show');
}

// Get the current active category button (to determine which category to add to)
function getCategoryFromActiveButton() {
    const activeButton = document.querySelector('.btn-group .btn-secondary.active');
    return activeButton ? activeButton.textContent : 'Fish'; // Default to 'Fish' if none is active
}

// Function to save or update a product (Add or Edit)
function saveOrUpdateProduct() {
    const name = $('#productName').val();
    const price = $('#productPrice').val();
    const stock = $('#productStock').val();
    const category = getCategoryFromActiveButton();

    if (editingProductId) {
        // Update existing product
        const product = products[category].find(p => p.id === editingProductId);
        product.name = name;
        product.price = price;
        product.stock = stock;
    } else {
        // Add new product
        const newProduct = { name, price, stock, id: Date.now() };
        products[category].push(newProduct);
    }

    updateProductList(category);
    $('#productModal').modal('hide');
}

// Function to delete a product
function deleteProduct() {
    const category = getCategoryFromActiveButton();
    products[category] = products[category].filter(p => p.id !== editingProductId); // Remove product from array
    updateProductList(category);
    $('#productModal').modal('hide');
}

// Initialize with default category (Fish)
$(document).ready(function() {
    updateProductList('Fish');
});
