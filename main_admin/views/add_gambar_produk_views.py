# --- IMPORTS ---

# Mengimpor model 'Produk' dan 'GambarProduk' dari file models.py.
from ..models import Produk, GambarProduk
# Mengimpor 'View', kelas dasar untuk Class-Based Views (CBV) yang fleksibel.
from django.views.generic import View
# Mengimpor shortcut dari Django: 'render' untuk template, 'get_object_or_404' untuk mengambil objek atau menampilkan error 404, dan 'redirect'.
from django.shortcuts import render, get_object_or_404, redirect
# Mengimpor model 'GambarProduk' dan form-form terkait.
from ..forms import GambarProduk, GambarProdukForm, GambarProdukFormSet
# Mixin untuk membatasi akses view hanya untuk pengguna yang sudah login.
from django.contrib.auth.mixins import LoginRequiredMixin
# Sebuah fungsi pabrik (factory function) untuk membuat FormSet yang terikat pada model induk dan anak (inline).
from django.forms import inlineformset_factory
# Digunakan untuk melakukan redirect setelah request POST berhasil, ini adalah praktik terbaik.
from django.http import HttpResponseRedirect
# Fungsi untuk membuat URL berdasarkan nama URL pattern di urls.py.
from django.urls import reverse


# --- CLASS-BASED VIEW UNTUK MENAMBAH GAMBAR ---

class AddProductImagesView(LoginRequiredMixin, View):
    """
    View berbasis kelas untuk menangani penambahan gambar baru ke produk yang sudah ada.
    Menggunakan View dasar agar kita bisa mendefinisikan logika untuk GET dan POST secara terpisah.
    """
    # Menentukan file template HTML yang akan digunakan oleh view ini.
    template_name = 'admin/product/add_gambar.html'

    # Method ini akan dieksekusi ketika ada HTTP GET request (saat pengguna pertama kali membuka halaman).
    def get(self, request, pk):
        # Mengambil objek 'Produk' berdasarkan 'pk' (primary key) yang ada di URL. Jika produk tidak ditemukan, akan menampilkan halaman 404 Not Found.
        produk = get_object_or_404(Produk, pk=pk)
        
        # Membuat instance dari 'GambarProdukFormSet'. Queryset diatur ke none() karena kita hanya ingin menampilkan form kosong untuk menambah gambar baru, bukan mengedit yang sudah ada.
        formset = GambarProdukFormSet(queryset=GambarProduk.objects.none())
        
        # Merender template dengan konteks yang dibutuhkan: judul halaman, objek produk, dan formset yang kosong.
        return render(request, self.template_name, {
            'title': f'Tambah Gambar untuk {produk.nama}',
            'produk': produk,
            'formset': formset
        })

    # Method ini akan dieksekusi ketika ada HTTP POST request (saat pengguna men-submit form).
    def post(self, request, pk):
        # Mengambil objek produk yang sama seperti di method get.
        produk = get_object_or_404(Produk, pk=pk)
        
        # Membuat instance formset dan mengisinya dengan data yang di-submit ('request.POST') dan file yang di-upload ('request.FILES').
        formset = GambarProdukFormSet(request.POST, request.FILES)

        # Memeriksa apakah semua data dalam formset valid.
        if formset.is_valid():
            # Jika valid, lakukan iterasi pada setiap form di dalam formset.
            for form in formset:
                # Memeriksa apakah form tersebut diisi (bukan form kosong tambahan).
                if form.cleaned_data:
                    # Menyimpan data form ke dalam objek model 'GambarProduk' tetapi belum menyimpannya ke database (commit=False).
                    gambar = form.save(commit=False)
                    # Mengatur hubungan ForeignKey: menghubungkan objek 'gambar' ini dengan 'produk' yang sedang diedit.
                    gambar.produk = produk
                    # Sekarang, simpan objek 'gambar' ke database dengan relasi yang sudah benar.
                    gambar.save()
            # Setelah semua form yang valid diproses dan disimpan, alihkan pengguna ke halaman daftar produk.
            return redirect('list_produk')

        # Jika formset tidak valid, render kembali template yang sama.
        # Formset sekarang akan berisi pesan-pesan error yang bisa ditampilkan di template untuk memberitahu pengguna apa yang salah.
        return render(request, self.template_name, {
            'title': f'Tambah Gambar untuk {produk.nama}',
            'produk': produk,
            'formset': formset
        })
    

# --- FUNCTION-BASED VIEW UNTUK MENGEDIT GAMBAR ---

def edit_product_images(request, pk):
    """
    View berbasis fungsi untuk mengelola (tambah/ubah/hapus) gambar
    dari produk yang sudah ada menggunakan inline formset.
    """
    # Mengambil objek produk yang akan diedit gambarnya.
    produk = get_object_or_404(Produk, pk=pk)
    
    # Membuat sebuah 'pabrik' FormSet. Ini cara yang sangat efisien untuk mengelola objek anak (GambarProduk) dari objek induk (Produk).
    ImageFormSet = inlineformset_factory(
        Produk,          # Model Induk
        GambarProduk,    # Model Anak
        form=GambarProdukForm, # Form yang digunakan untuk setiap item anak
        extra=1,         # Selalu tampilkan 1 form kosong tambahan untuk menambah gambar baru.
        can_delete=True  # Tampilkan checkbox di setiap form agar pengguna bisa menandai gambar untuk dihapus.
    )

    # Cek jika method request adalah POST (pengguna mengirimkan data).
    if request.method == 'POST':
        # Buat instance formset dengan data POST, file yang di-upload, dan kaitkan dengan instance 'produk' yang ada.
        formset = ImageFormSet(request.POST, request.FILES, instance=produk)
        # Validasi formset.
        if formset.is_valid():
            # Cukup panggil formset.save(). Django akan secara otomatis menangani:
            # - Menyimpan gambar baru yang ditambahkan.
            # - Memperbarui gambar yang diubah.
            # - Menghapus gambar yang ditandai untuk dihapus.
            formset.save()
            # Redirect kembali ke halaman detail produk setelah berhasil menyimpan. Ini mencegah submit ganda jika user me-refresh halaman.
            return HttpResponseRedirect(reverse('detail_produk', kwargs={'pk': produk.pk}))
    else: # Jika method request adalah GET (pengguna baru membuka halaman).
        # Buat instance formset yang terikat pada 'produk'. Ini akan secara otomatis mengisi formset dengan gambar-gambar yang sudah ada untuk produk ini.
        formset = ImageFormSet(instance=produk)

    # Render template dengan konteks yang dibutuhkan.
    return render(request, 'admin/product/update_gambar.html', {
        'title': f'Edit Gambar untuk {produk.nama}',
        'produk': produk,
        'formset': formset
    })