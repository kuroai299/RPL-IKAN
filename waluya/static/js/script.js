// Get DOM elements
const popup = document.getElementById('productPopup');
const closeBtn = document.querySelector('.popup-close');
const addProductBtn = document.querySelector('.add-product-btn');
const editBtn = document.querySelector('.edit-btn');
const decreaseBtn = document.getElementById('decreaseBtn');
const increaseBtn = document.getElementById('increaseBtn');
const quantityValue = document.getElementById('quantityValue');

// Show popup function
function showPopup(isEdit = false) {
    popup.style.display = 'flex';
    
    // If editing, we can pre-fill the form with existing data
    if (isEdit) {
        document.getElementById('addProductBtn').textContent = 'Update Produk';
        // Here you would typically populate the form with the product data
    } else {
        document.getElementById('addProductBtn').textContent = 'Tambah Produk';
    }
}

// Hide popup function
function hidePopup() {
    popup.style.display = 'none';
}

// Event listeners
addProductBtn.addEventListener('click', () => showPopup(false));
editBtn.addEventListener('click', () => showPopup(true));
closeBtn.addEventListener('click', hidePopup);

// Close popup when clicking outside
popup.addEventListener('click', (e) => {
    if (e.target === popup) {
        hidePopup();
    }
});

// Category button functionality
document.querySelectorAll('.category-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Remove active class from all buttons
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        // Add active class to clicked button
        button.classList.add('active');
    });
});

// Quantity control
let quantity = 5;

decreaseBtn.addEventListener('click', () => {
    if (quantity > 1) {
        quantity--;
        quantityValue.textContent = quantity;
    }
});

increaseBtn.addEventListener('click', () => {
    quantity++;
    quantityValue.textContent = quantity;
});

// Form submission (just for demonstration)
document.getElementById('addProductBtn').addEventListener('click', () => {
    alert('Product saved successfully!');
    hidePopup();
});

// Delete button (just for demonstration)
document.querySelector('.delete-btn').addEventListener('click', () => {
    if (confirm('Are you sure you want to delete this product?')) {
        alert('Product deleted successfully!');
        hidePopup();
    }
});
