// File: static/product/admin/js/price-formatter.js

document.addEventListener('DOMContentLoaded', function() {
    // Fungsi untuk memformat angka dengan pemisah ribuan
    function formatNumber(input) {
        let value = input.value.replace(/[^0-9]/g, '');
        
        if (value === '') {
            input.value = '';
            return;
        }
        
        let number = parseInt(value, 10);
        input.value = number.toLocaleString('id-ID');
    }

    // Cari SEMUA input yang memiliki kelas 'price-format'
    const priceInputs = document.querySelectorAll('.price-format');

    // Terapkan fungsi ke setiap input yang ditemukan
    priceInputs.forEach(function(input) {
        input.addEventListener('input', function() {
            formatNumber(this);
        });
        // Format juga nilai awal saat halaman dimuat (untuk halaman edit)
        formatNumber(input);
    });
});
