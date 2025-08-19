
document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('whatsapp-contact-form');

    contactForm.addEventListener('submit', function(event) {
        // 1. Mencegah form mengirim data secara normal
        event.preventDefault();

        // GANTI DENGAN NOMOR WA ANDA (diawali 62)
        const phoneNumber = '6285731290116'; 

        // 2. Ambil data dari setiap input
        const name = document.getElementById('contact_name').value;
        const email = document.getElementById('contact_email').value;
        const number = document.getElementById('contact_number').value;
        const message = document.getElementById('contact_message').value;

        // 3. Susun pesan yang akan dikirim
        const whatsappMessage = `Halo, saya ingin bertanya.\n\n*Nama:* ${name}\n*Email:* ${email}\n*Nomor HP:* ${number}\n\n*Pesan:*\n${message}`;

        // 4. Buat URL WhatsApp
        // encodeURIComponent() akan mengubah spasi dan karakter lain menjadi format URL
        const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(whatsappMessage)}`;

        // 5. Buka WhatsApp di tab baru
        window.open(whatsappUrl, '_blank');
    });
});