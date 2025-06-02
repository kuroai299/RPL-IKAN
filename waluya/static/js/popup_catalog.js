let preveiwContainer = document.querySelector('.product-preview');
let previewBox = preveiwContainer.querySelectorAll('.preview');

// Ketika pengguna mengklik produk (card), buka popup
document.querySelectorAll('.card-container .card').forEach(card => {
    card.onclick = () => {
        preveiwContainer.style.display = 'flex'; // Menampilkan container popup
        let target = card.getAttribute('data-target'); // Ambil data-target dari card yang diklik
        previewBox.forEach(preview => {
            let previewTarget = preview.getAttribute('data-target'); // Cocokkan dengan preview yang sesuai
            if (target === previewTarget) {
                preview.classList.add('active'); // Menampilkan preview yang sesuai
            } else {
                preview.classList.remove('active'); // Menyembunyikan preview lainnya
            }
        });
    };
});

// Menutup popup ketika klik tombol close (fa-times)
previewBox.forEach(preview => {
    const closeBtn = preview.querySelector('.fa-times'); // Ambil tombol close
    closeBtn.onclick = () => {
        preview.classList.remove('active'); // Menyembunyikan preview
        preveiwContainer.style.display = 'none'; // Menyembunyikan container popup
    };
});

// Menutup popup juga jika area di luar preview diklik (untuk menutup popup)
preveiwContainer.onclick = (event) => {
    if (event.target === preveiwContainer) {
        preveiwContainer.style.display = 'none'; // Menyembunyikan container popup jika area luar diklik
        previewBox.forEach(preview => preview.classList.remove('active')); // Menyembunyikan semua preview
    }
};
console.log("JS file loaded successfully");

// Menangani klik tombol filter untuk menampilkan dan menyembunyikan filter section
document.getElementById('filterButton').addEventListener('click', function() {
    var filterSection = document.getElementById('filterSection');
    filterSection.classList.toggle('active');  // Menyembunyikan/menampilkan filter section
});
