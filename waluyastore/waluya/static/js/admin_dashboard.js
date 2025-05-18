// DOM Elements
const openPopupBtn = document.getElementById("openPopupBtn");
const closePopupBtn = document.getElementById("closePopupBtn");
const productPopup = document.getElementById("productPopup");
const productForm = document.getElementById("productForm");
const addProductBtn = document.getElementById("addProductBtn");
const deleteBtn = document.getElementById("deleteBtn");
const decreaseBtn = document.getElementById("decreaseBtn");
const increaseBtn = document.getElementById("increaseBtn");
const quantityValue = document.getElementById("quantityValue");
const productStock = document.getElementById("productStock");
const productImage = document.getElementById("productImage");
const imagePreview = document.getElementById("imagePreview");
const productName = document.getElementById("productName");
const productDescription = document.getElementById("productDescription");
const productPrice = document.getElementById("productPrice");
const productCategory = document.getElementById("productCategory");
const productId = document.getElementById("productId");
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const productsList = document.getElementById("productsList");

// Category-specific fields containers
const fishFields = document.getElementById("fishFields");
const medicineFields = document.getElementById("medicineFields");
const stuffFields = document.getElementById("stuffFields");
const foodFields = document.getElementById("foodFields");

// Delete confirmation modal
const deleteConfirmModal = document.getElementById("deleteConfirmModal");
const deleteProductName = document.getElementById("deleteProductName");
const cancelDeleteBtn = document.getElementById("cancelDeleteBtn");
const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

// State
let currentProductId = null;
let quantity = 5;
let currentCategory = getUrlParameter('category') || 'Fish';

// Get URL parameter
function getUrlParameter(name) {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get(name);
}

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Show popup function with animation
function showPopup(isEdit = false, productId = null, category = null, productData = null) {
    // Show the popup
    productPopup.style.display = "flex";

    // Add animation class
    document.body.style.overflow = "hidden";

    // Reset form first
    resetForm();

    // If editing, we can pre-fill the form with existing data
    if (isEdit && productId) {
        currentProductId = productId;
        if (productId.value !== undefined) {
            productId.value = productId;
        }
        addProductBtn.textContent = "Update Produk";
        deleteBtn.style.display = "flex";

        // If we have product data from the button attributes
        if (productData) {
            fillFormWithProductData(productData);
        } else {
            // Fetch product data from the server
            fetch(`/custom-admin/edit_product/${productId}/?category=${category}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success && data.product) {
                    fillFormWithProductData(data.product);
                } else {
                    showToast('Failed to load product data', 'error');
                    hidePopup();
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Failed to load product data', 'error');
                hidePopup();
            });
        }
    } else {
        currentProductId = null;
        if (productId && productId.value !== undefined) {
            productId.value = '';
        }
        addProductBtn.textContent = "Tambah Produk";
        deleteBtn.style.display = "none";

        // If a category is provided, select it in the dropdown
        if (category) {
            selectCategory(category);
            updateCategoryFields();
        }
    }
}

// Hide popup function with animation
function hidePopup() {
    // Add closing animation
    productPopup.style.opacity = "0";
    productPopup.style.transform = "scale(0.95)";

    // After animation completes, hide the popup
    setTimeout(() => {
        productPopup.style.display = "none";
        productPopup.style.opacity = "1";
        productPopup.style.transform = "scale(1)";
        document.body.style.overflow = "auto";
        resetForm();
    }, 200);
}

// Reset form function
function resetForm() {
    productForm.reset();
    imagePreview.innerHTML = "<p>no image</p>";
    productName.value = "";
    productDescription.value = "";
    productPrice.value = "";
    productCategory.selectedIndex = 0;
    quantity = 5;
    quantityValue.textContent = quantity;
    productStock.value = quantity;
    currentProductId = null;
    
    // Hide all category-specific fields
    fishFields.style.display = "none";
    medicineFields.style.display = "none";
    stuffFields.style.display = "none";
    foodFields.style.display = "none";
}

// Fill form with product data
function fillFormWithProductData(data) {
    productName.value = data.name || "";
    productDescription.value = data.description || "";
    productPrice.value = data.price || "";

    // Set quantity
    quantity = parseInt(data.stock) || 5;
    quantityValue.textContent = quantity;
    productStock.value = quantity;

    // Select the correct category
    selectCategory(data.category);
    updateCategoryFields();

    // Set category-specific fields
    if (data.category === 'Fish') {
        document.getElementById('fishSize').value = data.size || 'kecil';
        document.getElementById('fishColor').value = data.color || 'gelap';
    } else if (data.category === 'FishMedicine') {
        document.getElementById('medicineType').value = data.medicine_type || 'herbal';
    } else if (data.category === 'AquariumStuff') {
        document.getElementById('stuffType').value = data.stuff_type || 'filter';
    } else if (data.category === 'FishFood') {
        document.getElementById('foodType').value = data.food_type || 'organik';
    }

    // If there's an image URL in the data, show it
    if (data.image) {
        imagePreview.innerHTML = `<img src="${data.image}" alt="${data.name}">`;
    }
}

// Select category in dropdown
function selectCategory(category) {
    if (!category) return;

    for (let i = 0; i < productCategory.options.length; i++) {
        if (productCategory.options[i].value === category) {
            productCategory.selectedIndex = i;
            break;
        }
    }
}

// Update category-specific fields visibility
function updateCategoryFields() {
    // Hide all category fields
    fishFields.style.display = 'none';
    medicineFields.style.display = 'none';
    stuffFields.style.display = 'none';
    foodFields.style.display = 'none';
    
    // Show fields based on selected category
    const category = productCategory.value;
    if (category === 'Fish') {
        fishFields.style.display = 'block';
    } else if (category === 'FishMedicine') {
        medicineFields.style.display = 'block';
    } else if (category === 'AquariumStuff') {
        stuffFields.style.display = 'block';
    } else if (category === 'FishFood') {
        foodFields.style.display = 'block';
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    // Remove any existing toasts
    const existingToast = document.querySelector('.toast-message');
    if (existingToast) {
        existingToast.remove();
    }
    
    // Create toast element
    const toast = document.createElement('div');
    toast.className = `toast-message ${type}`;
    toast.textContent = message;
    
    // Add to document
    document.body.appendChild(toast);
    
    // Show toast with animation
    setTimeout(() => {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    }, 10);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toast.style.transform = 'translateY(-20px)';
        toast.style.opacity = '0';
        
        // Remove from DOM after animation
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, 3000);
}

// Open delete confirmation modal
function openDeleteConfirmModal(productId, productName) {
    currentProductId = productId;
    deleteProductName.textContent = productName;
    deleteConfirmModal.style.display = "flex";
    deleteConfirmModal.style.opacity = "1";
    deleteConfirmModal.querySelector('.confirm-content').style.transform = "scale(1)";
}

// Close delete confirmation modal
function closeDeleteConfirmModal() {
    deleteConfirmModal.style.opacity = "0";
    deleteConfirmModal.querySelector('.confirm-content').style.transform = "scale(0.9)";
    setTimeout(() => {
        deleteConfirmModal.style.display = "none";
    }, 300);
}

// Delete product
function deleteProduct() {
    if (!currentProductId) {
        showToast('No product selected for deletion', 'error');
        return;
    }
    
    // Show loading state
    confirmDeleteBtn.textContent = "Deleting...";
    confirmDeleteBtn.disabled = true;
    
    // Send delete request
    fetch(`/custom-admin/delete_product/${currentProductId}/?category=${currentCategory}`, {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Failed to delete product');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            showToast(data.message || 'Product deleted successfully');
            closeDeleteConfirmModal();
            // Reload the page after a short delay
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Failed to delete product', 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showToast(error.message || 'An error occurred', 'error');
    })
    .finally(() => {
        // Reset button state
        confirmDeleteBtn.textContent = "Delete";
        confirmDeleteBtn.disabled = false;
    });
}

// Load products from API
function loadProducts(category, searchQuery = '') {
    productsList.innerHTML = `
        <div class="loading-indicator">
            <div class="spinner"></div>
            <p>Loading products...</p>
        </div>
    `;
    
    let url = `/custom-admin/dashboard/?category=${category}&format=json`;
    if (searchQuery) {
        url += `&search=${encodeURIComponent(searchQuery)}`;
    }
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.products && data.products.length > 0) {
                displayProducts(data.products, category);
            } else {
                showEmptyState();
            }
        })
        .catch(error => {
            console.error('Error:', error);
            productsList.innerHTML = `
                <div class="error-state">
                    <div class="error-icon">❌</div>
                    <p>Failed to load products.</p>
                    <p class="error-hint">Please try refreshing the page.</p>
                </div>
            `;
        });
}

// Display products in the list
function displayProducts(products, category) {
    productsList.innerHTML = '';
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        
        productCard.innerHTML = `
            <div class="product-card-content">
                <div class="product-image-container">
                    ${product.image ? 
                        `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                        `<div class="no-image">No Image</div>`
                    }
                </div>
                <div class="product-info">
                    <h3 class="product-title">${product.name}</h3>
                    <p class="product-description">${product.description.substring(0, 100)}${product.description.length > 100 ? '...' : ''}</p>
                    <div class="product-meta">
                        <span class="product-price">Rp ${product.price}</span>
                        <span class="product-stock">Stock: ${product.stock}</span>
                    </div>
                    <div class="product-actions">
                        <button class="edit-btn" data-product-id="${product.id}" data-category="${category}">Edit</button>
                        <button class="delete-btn" data-product-id="${product.id}" data-name="${product.name}">Delete</button>
                    </div>
                </div>
            </div>
        `;
        
        productsList.appendChild(productCard);
        
        // Add event listeners to buttons
        const editBtn = productCard.querySelector('.edit-btn');
        const deleteBtn = productCard.querySelector('.delete-btn');
        
        editBtn.addEventListener('click', () => showPopup(true, product.id, category));
        deleteBtn.addEventListener('click', () => openDeleteConfirmModal(product.id, product.name));
    });
}

// Show empty state when no products
function showEmptyState() {
    productsList.innerHTML = `
        <div class="empty-state">
            <div class="empty-icon">📦</div>
            <p>No products available.</p>
            <p class="empty-hint">Click "Add Product" to get started.</p>
        </div>
    `;
}

// Search products
function searchProducts() {
    const query = searchInput.value.trim();
    if (query === '') {
        window.location.href = `/custom-admin/dashboard/?category=${currentCategory}`;
    } else {
        loadProducts(currentCategory, query);
    }
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function() {
    // Bind event for all edit buttons
    document.querySelectorAll(".edit-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const productId = btn.dataset.productId;
            const category = btn.dataset.category;
            showPopup(true, productId, category);
        });
    });

    // Bind event for all delete buttons
    document.querySelectorAll(".delete-btn").forEach((btn) => {
        btn.addEventListener("click", () => {
            const productId = btn.dataset.productId;
            const productName = btn.dataset.name;
            openDeleteConfirmModal(productId, productName);
        });
    });

    // Focus animation for inputs
    const inputs = document.querySelectorAll("input, textarea, select");

    inputs.forEach((input) => {
        input.addEventListener("focus", () => {
            input.parentElement.classList.add("focused");
        });

        input.addEventListener("blur", () => {
            input.parentElement.classList.remove("focused");
        });
    });
});

// Open popup button
if (openPopupBtn) {
    openPopupBtn.addEventListener("click", () => showPopup(false, null, currentCategory));
}

// Close popup button
if (closePopupBtn) {
    closePopupBtn.addEventListener("click", hidePopup);
}

// Close popup when clicking outside
if (productPopup) {
    productPopup.addEventListener("click", (e) => {
        if (e.target === productPopup) {
            hidePopup();
        }
    });
}

// Category dropdown change
if (productCategory) {
    productCategory.addEventListener('change', updateCategoryFields);
}

// Quantity control with smooth animation
if (decreaseBtn) {
    decreaseBtn.addEventListener("click", () => {
        if (quantity > 1) {
            quantity--;
            quantityValue.textContent = quantity;
            productStock.value = quantity;

            // Add animation
            quantityValue.style.transform = "scale(0.8)";
            setTimeout(() => {
                quantityValue.style.transform = "scale(1)";
            }, 100);
        }
    });
}

if (increaseBtn) {
    increaseBtn.addEventListener("click", () => {
        quantity++;
        quantityValue.textContent = quantity;
        productStock.value = quantity;

        // Add animation
        quantityValue.style.transform = "scale(1.2)";
        setTimeout(() => {
            quantityValue.style.transform = "scale(1)";
        }, 100);
    });
}

// Image upload handling with preview animation
if (productImage) {
    productImage.addEventListener("change", (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();

            reader.onload = (event) => {
                // Create image with fade-in effect
                imagePreview.innerHTML = `<img src="${event.target.result}" alt="Product Image" style="opacity: 0; transition: opacity 0.3s ease;">`;

                // Fade in the image
                setTimeout(() => {
                    imagePreview.querySelector("img").style.opacity = "1";
                }, 50);
            };

            reader.readAsDataURL(file);
        }
    });
}

// Character counter for description with color change
if (productDescription) {
    productDescription.addEventListener("input", function () {
        const maxLength = this.getAttribute("maxlength");
        const currentLength = this.value.length;
        const charCountElement = this.parentElement.querySelector(".char-count");
        if (charCountElement) {
            const percentage = (currentLength / maxLength) * 100;

            charCountElement.textContent = `${currentLength}/${maxLength} characters`;

            // Change color based on length
            if (percentage >= 90) {
                charCountElement.style.color = "#ef4444"; // Red
                charCountElement.style.fontWeight = "600";
            } else if (percentage >= 75) {
                charCountElement.style.color = "#f59e0b"; // Amber
                charCountElement.style.fontWeight = "500";
            } else {
                charCountElement.style.color = "#6b7280"; // Gray
                charCountElement.style.fontWeight = "400";
            }
        }
    });
}

// Price input validation - only allow numbers and decimal point
if (productPrice) {
    productPrice.addEventListener("input", function (e) {
        // Remove any non-numeric characters except decimal point and comma
        let value = this.value.replace(/[^\d.,]/g, "");

        // Ensure only one decimal separator exists
        let decimalCount = 0;
        value = value.replace(/[.,]/g, (match) => {
            decimalCount++;
            // Convert all separators to period for consistency
            return decimalCount === 1 ? "." : "";
        });

        // Update the input value
        this.value = value;
    });
}

// Form submission
if (productForm) {
    productForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        console.log("Form submission started");
        
        // Validate form
        if (!validateForm()) {
            console.log("Form validation failed");
            return;
        }
        
        // Show loading state
        addProductBtn.textContent = "Saving...";
        addProductBtn.disabled = true;
        
        // Get form data
        const formData = new FormData(this);
        
        // Log form data for debugging
        console.log("Submitting form with data:");
        for (let [key, value] of formData.entries()) {
            console.log(key + ": " + (value instanceof File ? `File: ${value.name}` : value));
        }
        
        // Determine URL based on whether adding or editing
        let url = '/custom-admin/add_product/';
        
        if (currentProductId) {
            url = `/custom-admin/edit_product/${currentProductId}/?category=${productCategory.value}`;
        }
        
        console.log("Submitting to URL:", url);
        
        // Send AJAX request
        fetch(url, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'same-origin'
        })
        .then(response => {
            console.log("Response received:", response);
            console.log("Response status:", response.status);
            console.log("Response headers:", Array.from(response.headers.entries()));
            
            // Try to get the response text first
            return response.text().then(text => {
                console.log("Raw response text:", text);
                
                // Try to parse as JSON if possible
                try {
                    const data = JSON.parse(text);
                    console.log("Parsed JSON response:", data);
                    
                    if (!response.ok) {
                        if (data.errors) {
                            console.error("Validation errors:", data.errors);
                            let errorMessage = "Form validation failed: ";
                            for (const [field, error] of Object.entries(data.errors)) {
                                errorMessage += `${field}: ${error}; `;
                            }
                            throw new Error(errorMessage);
                        } else {
                            throw new Error(data.error || `Failed to save product (${response.status})`);
                        }
                    }
                    
                    // Success case
                    console.log("Form submission successful");
                    showToast(data.message || "Product saved successfully");
                    hidePopup();
                    
                    // Reload the page after a short delay
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                    
                    return data;
                } catch (e) {
                    console.error("Error parsing JSON:", e);
                    if (!response.ok) {
                        throw new Error(`Failed to save product (${response.status}): ${text}`);
                    }
                    
                    // If we can't parse JSON but the response is OK, assume success
                    if (response.ok) {
                        showToast("Product saved successfully");
                        hidePopup();
                        
                        // Reload the page after a short delay
                        setTimeout(() => {
                            window.location.reload();
                        }, 1000);
                    }
                    
                    return { success: response.ok, error: response.ok ? null : "Invalid JSON response" };
                }
            });
        })
        .catch(error => {
            console.error("Fetch error:", error);
            showToast(error.message || "Failed to save product", "error");
        })
        .finally(() => {
            console.log("Form submission completed");
            // Reset button state
            addProductBtn.textContent = currentProductId ? "Update Produk" : "Tambah Produk";
            addProductBtn.disabled = false;
        });
    });
}

// Delete button in form
if (deleteBtn) {
    deleteBtn.addEventListener('click', function() {
        if (currentProductId) {
            // Get product name
            const name = productName.value || 'this product';
            openDeleteConfirmModal(currentProductId, name);
        }
    });
}

// Delete confirmation modal buttons
if (cancelDeleteBtn) {
    cancelDeleteBtn.addEventListener('click', closeDeleteConfirmModal);
}

if (confirmDeleteBtn) {
    confirmDeleteBtn.addEventListener('click', deleteProduct);
}

// Search functionality
if (searchBtn) {
    searchBtn.addEventListener('click', searchProducts);
}

if (searchInput) {
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            searchProducts();
        }
    });
}

// Form validation
function validateForm() {
    let isValid = true;
    
    // Reset previous validation styles
    document.querySelectorAll(".form-group").forEach((group) => {
        group.classList.remove("error");
    });
    
    // Remove any existing error messages
    document.querySelectorAll(".error-message").forEach((msg) => {
        msg.remove();
    });
    
    // Validate name
    if (!productName.value.trim()) {
        showValidationError(productName, "Please enter a product name");
        isValid = false;
    }
    
    // Validate description
    if (!productDescription.value.trim()) {
        showValidationError(productDescription, "Please enter a product description");
        isValid = false;
    }
    
    // Validate price
    if (!productPrice.value.trim()) {
        showValidationError(productPrice, "Please enter a product price");
        isValid = false;
    } else {
        // Convert to a standard number format for validation
        const priceValue = productPrice.value.replace(/,/g, ".");
        if (isNaN(Number.parseFloat(priceValue)) || !isFinite(priceValue)) {
            showValidationError(productPrice, "Price must be a valid number");
            isValid = false;
        }
    }
    
    // Validate category
    if (productCategory.selectedIndex === 0) {
        showValidationError(productCategory, "Please select a category");
        isValid = false;
    }
    
    return isValid;
}

// Show validation error
function showValidationError(element, message) {
    // Add error class to parent
    const formGroup = element.closest(".form-group");
    if (formGroup) {
        formGroup.classList.add("error");
        
        // Create error message
        const errorMsg = document.createElement("div");
        errorMsg.className = "error-message";
        errorMsg.textContent = message;
        
        // Add after the input
        element.parentNode.insertBefore(errorMsg, element.nextSibling);
        
        // Shake animation
        element.style.animation = "shake 0.5s ease";
        setTimeout(() => {
            element.style.animation = "";
        }, 500);
    }
}

// Add styles for new elements
const style = document.createElement("style");
style.textContent = `
    .action-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
    }
    
    .search-container {
        display: flex;
        align-items: center;
        position: relative;
        width: 300px;
    }
    
    .search-container input {
        width: 100%;
        padding: 10px 40px 10px 16px;
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        font-size: 14px;
    }
    
    .search-container button {
        position: absolute;
        right: 8px;
        background: none;
        border: none;
        cursor: pointer;
        color: var(--text-light);
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .search-container button svg {
        width: 20px;
        height: 20px;
    }
    
    .messages {
        margin-bottom: 24px;
    }
    
    .message {
        padding: 12px 16px;
        border-radius: var(--radius-md);
        margin-bottom: 8px;
        font-size: 14px;
    }
    
    .message.success {
        background-color: #d1fae5;
        color: #065f46;
    }
    
    .message.error {
        background-color: #fee2e2;
        color: #b91c1c;
    }
    
    .message.info {
        background-color: #dbeafe;
        color: #1e40af;
    }
    
    .message.warning {
        background-color: #fef3c7;
        color: #92400e;
    }
    
    .product-actions {
        display: flex;
        gap: 8px;
    }
    
    .product-actions .edit-btn,
    .product-actions .delete-btn {
        flex: 1;
        padding: 8px 12px;
        font-size: 14px;
    }
    
    .product-actions .delete-btn {
        background-color: #fee2e2;
        color: #b91c1c;
        border: none;
        border-radius: var(--radius-md);
        cursor: pointer;
        transition: var(--transition);
    }
    
    .product-actions .delete-btn:hover {
        background-color: #fecaca;
    }
    
    .no-image {
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f3f4f6;
        color: var(--text-light);
        font-size: 14px;
    }
    
    .confirm-dialog {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: none;
        justify-content: center;
        align-items: center;
        z-index: 2000;
        opacity: 0;
        transition: opacity 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .confirm-content {
        background-color: white;
        border-radius: 12px;
        padding: 24px;
        width: 90%;
        max-width: 400px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        transform: scale(0.9);
        transition: transform 0.3s ease;
    }
    
    .confirm-content h3 {
        margin-bottom: 16px;
        color: #1e40af;
        font-size: 20px;
    }
    
    .confirm-content p {
        margin-bottom: 24px;
        color: #4b5563;
        line-height: 1.5;
    }
    
    .confirm-actions {
        display: flex;
        justify-content: flex-end;
        gap: 12px;
    }
    
    .cancel-btn {
        padding: 10px 16px;
        border-radius: 8px;
        border: 1px solid #d1d5db;
        background-color: white;
        color: #4b5563;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .cancel-btn:hover {
        background-color: #f3f4f6;
    }
    
    .confirm-btn {
        padding: 10px 16px;
        border-radius: 8px;
        border: none;
        background-color: #ef4444;
        color: white;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .confirm-btn:hover {
        background-color: #dc2626;
    }
    
    .form-group.error input,
    .form-group.error select,
    .form-group.error textarea {
        border: 2px solid #ef4444;
        background-color: #fef2f2;
    }
    
    .error-message {
        color: #ef4444;
        font-size: 12px;
        margin-top: 4px;
        font-weight: 500;
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .toast-message {
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 24px;
        border-radius: 8px;
        color: white;
        font-weight: 500;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 2000;
        transform: translateY(-20px);
        opacity: 0;
        transition: all 0.3s ease;
    }
    
    .toast-message.success {
        background-color: #10b981;
    }
    
    .toast-message.error {
        background-color: #ef4444;
    }
    
    .toast-message.warning {
        background-color: #f59e0b;
    }
    
    .loading-indicator {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px;
        width: 100%;
    }
    
    .spinner {
        width: 40px;
        height: 40px;
        border: 4px solid var(--primary-lightest);
        border-top: 4px solid var(--primary);
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-bottom: 16px;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .logout-icon {
        margin-top: auto;
        margin-bottom: 20px;
    }
`;
document.head.appendChild(style);