// File: static/admin/assets/js/auth-custom.js

// Tunggu sampai dokumen siap
$(document).ready(function() {
    // Cari semua tombol di dalam grup input password
    $('.auth-pass-inputgroup button').on('click', function() {
        // Cari input field yang ada di sebelahnya
        var passwordInput = $(this).prev('input');
        
        // Cek tipe input saat ini
        if (passwordInput.attr('type') === 'password') {
            // Jika tipenya password, ubah menjadi text
            passwordInput.attr('type', 'text');
            // Ganti ikon mata menjadi tercoret
            $(this).find('i').removeClass('mdi-eye-outline').addClass('mdi-eye-off-outline');
        } else {
            // Jika tipenya text, ubah kembali menjadi password
            passwordInput.attr('type', 'password');
            // Ganti ikon mata kembali normal
            $(this).find('i').removeClass('mdi-eye-off-outline').addClass('mdi-eye-outline');
        }
    });
});
