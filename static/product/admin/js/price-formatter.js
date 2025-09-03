// File: static/product/admin/js/price-formatter.js

document.addEventListener('DOMContentLoaded', function() {
    // Fungsi untuk memformat angka dengan pemisah ribuan
    function formatNumber(input) {
        // Hapus semua karakter non-digit
        let value = input.value.replace(/[^0-9]/g, '');
        
        if (value === '') {
            input.value = '';
            return;
        }
        
        let number = parseInt(value, 10);
        input.value = number.toLocaleString('id-ID');
    }

    // Ambil form dan semua input harga
    const productForm = document.getElementById('product-form');
    const priceInputs = document.querySelectorAll('.price-format');

    // Terapkan fungsi format ke setiap input saat diketik
    priceInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            formatNumber(this);
        });
        // Format juga nilai awal saat halaman dimuat (untuk halaman edit)
        formatNumber(input);
    });

    // --- BAGIAN BARU DITAMBAHKAN DI SINI ---
    // Saat form akan di-submit, jalankan fungsi pembersihan
    if (productForm) {
        productForm.addEventListener('submit', function() {
            priceInputs.forEach(function(input) {
                // Ambil nilai yang diformat (misal: "150.000")
                // dan hapus semua titiknya. Hasilnya "150000"
                input.value = input.value.replace(/\./g, '');
            });
        });
    }
});