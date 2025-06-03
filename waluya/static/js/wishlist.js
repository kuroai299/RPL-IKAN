// wishlist.js - Perbaikan untuk mencegah double event binding
document.addEventListener('DOMContentLoaded', function() {
    // PENTING: Hapus event listener yang sudah ada jika ada
    const existingButtons = document.querySelectorAll('[id="add-to-wishlist"], [id="remove-from-wishlist"], .add-to-wishlist-btn, .remove-from-wishlist-btn');
    existingButtons.forEach(button => {
        // Clone node untuk menghapus semua event listener
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
    });
    
    // Flag untuk mencegah multiple requests
    let isProcessing = false;
    
    // Gunakan event delegation untuk menangani semua tombol wishlist
    document.addEventListener('click', function(e) {
        // Cek apakah yang diklik adalah tombol add-to-wishlist atau childnya
        const addButton = e.target.closest('[id="add-to-wishlist"], .add-to-wishlist-btn');
        if (addButton) {
            e.preventDefault();
            e.stopPropagation(); // Penting: Hentikan event propagation
            
            console.log('Add to wishlist clicked'); // Debug
            
            if (isProcessing) {
                console.log('Request sedang diproses, abaikan klik'); // Debug
                return;
            }
            
            isProcessing = true;
            addButton.disabled = true;
            
            const productId = addButton.dataset.productId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            console.log('Sending request for product ID:', productId); // Debug
            
            fetch(`/add_to_wishlist/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response received:', data); // Debug
                
                if (data.success) {
                    // Update button
                    addButton.innerHTML = '<i class="fas fa-heart"></i> Hapus dari Wishlist';
                    addButton.classList.add('in-wishlist');
                    addButton.dataset.wishlistId = data.wishlist_id;
                    
                    // Update class dan ID
                    if (addButton.id === 'add-to-wishlist') {
                        addButton.id = 'remove-from-wishlist';
                    }
                    if (addButton.classList.contains('add-to-wishlist-btn')) {
                        addButton.classList.replace('add-to-wishlist-btn', 'remove-from-wishlist-btn');
                    }
                    
                    showMessage('success', data.message);
                } else {
                    showMessage('error', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('error', 'Terjadi kesalahan saat menambahkan ke wishlist');
            })
            .finally(() => {
                setTimeout(() => {
                    isProcessing = false;
                    addButton.disabled = false;
                }, 1000); // Tambahkan delay 1 detik untuk mencegah double click
            });
        }
        
        // Cek apakah yang diklik adalah tombol remove-from-wishlist atau childnya
        const removeButton = e.target.closest('[id="remove-from-wishlist"], .remove-from-wishlist-btn');
        if (removeButton) {
            e.preventDefault();
            e.stopPropagation(); // Penting: Hentikan event propagation
            
            console.log('Remove from wishlist clicked'); // Debug
            
            if (isProcessing) {
                console.log('Request sedang diproses, abaikan klik'); // Debug
                return;
            }
            
            isProcessing = true;
            removeButton.disabled = true;
            
            const wishlistId = removeButton.dataset.wishlistId;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            console.log('Sending request for wishlist ID:', wishlistId); // Debug
            
            fetch(`/remove_from_wishlist/${wishlistId}/`, {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => response.json())
            .then(data => {
                console.log('Response received:', data); // Debug
                
                if (data.success) {
                    // Cek apakah sedang di halaman wishlist
                    if (window.location.pathname.includes('wishlist')) {
                        // Hapus card dari halaman wishlist
                        const card = removeButton.closest('.wishlist-card');
                        if (card) {
                            card.style.transition = 'all 0.5s';
                            card.style.opacity = '0';
                            card.style.transform = 'scale(0.8)';
                            
                            setTimeout(() => {
                                card.remove();
                                
                                // Cek apakah masih ada item
                                const remainingCards = document.querySelectorAll('.wishlist-card');
                                if (remainingCards.length === 0) {
                                    location.reload();
                                }
                            }, 500);
                        }
                    } else {
                        // Update button di halaman produk
                        removeButton.innerHTML = '<i class="far fa-heart"></i> Tambah ke Wishlist';
                        removeButton.classList.remove('in-wishlist');
                        removeButton.dataset.wishlistId = '';
                        
                        // Update class dan ID
                        if (removeButton.id === 'remove-from-wishlist') {
                            removeButton.id = 'add-to-wishlist';
                        }
                        if (removeButton.classList.contains('remove-from-wishlist-btn')) {
                            removeButton.classList.replace('remove-from-wishlist-btn', 'add-to-wishlist-btn');
                        }
                    }
                    
                    showMessage('success', data.message);
                } else {
                    showMessage('error', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showMessage('error', 'Terjadi kesalahan saat menghapus dari wishlist');
            })
            .finally(() => {
                setTimeout(() => {
                    isProcessing = false;
                    removeButton.disabled = false;
                }, 1000); // Tambahkan delay 1 detik untuk mencegah double click
            });
        }
    }, { capture: true }); // Gunakan capture phase untuk menangkap event sebelum bubbling
    
    // Function to show messages
    function showMessage(type, message) {
        let messagesContainer = document.querySelector('.messages');
        
        if (!messagesContainer) {
            messagesContainer = document.createElement('div');
            messagesContainer.className = 'messages container';
            
            const header = document.querySelector('header');
            if (header) {
                header.parentNode.insertBefore(messagesContainer, header.nextSibling);
            } else {
                document.body.prepend(messagesContainer);
            }
        }
        
        const messageElement = document.createElement('div');
        messageElement.className = type;
        messageElement.textContent = message;
        
        messagesContainer.appendChild(messageElement);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            messageElement.remove();
            if (messagesContainer.children.length === 0) {
                messagesContainer.remove();
            }
        }, 5000);
    }
});