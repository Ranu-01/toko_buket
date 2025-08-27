# filename: views_kategori.py

# --- IMPORTS ---
# Mengimpor fungsi dasar Django: 'render' untuk merender template HTML dan 'redirect' untuk mengalihkan pengguna.
from django.shortcuts import render, redirect
# Mengimpor Class-Based Views (CBV) generik untuk menampilkan daftar (ListView), membuat (CreateView), menghapus (DeleteView), dan memperbarui (UpdateView) data.
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
# Mengimpor 'reverse_lazy' dan 'reverse' untuk membuat URL dari nama URL pattern di urls.py.
from django.urls import reverse_lazy, reverse
# Mengimpor model 'Kategori' dan 'Produk' dari file models.py.
from ..models import Kategori, Produk
# Mixin untuk memastikan view hanya bisa diakses oleh pengguna yang sudah login.
from django.contrib.auth.mixins import LoginRequiredMixin
# Mengimpor Model dan Form. Catatan: Mengimpor model Kategori dan Produk di sini bisa jadi redundan karena sudah diimpor di atas.
from ..forms import Kategori, Produk, KategoriForm


# --- CLASS-BASED VIEWS UNTUK KATEGORI ---

class KategoriListView(LoginRequiredMixin, ListView):
    """
    View untuk menampilkan daftar semua kategori beserta produk di dalamnya.
    """
    # Menentukan model utama yang akan ditampilkan, yaitu Kategori.
    model = Kategori
    # Menentukan file template HTML yang akan digunakan untuk merender halaman ini.
    template_name = 'admin/detail_kategori.html'
    # Menentukan nama variabel di dalam template yang akan berisi daftar semua objek kategori.
    context_object_name = 'semua_kategori'

    # Method ini untuk menambahkan data custom ke dalam konteks yang dikirim ke template.
    def get_context_data(self, **kwargs):
        # Memanggil method asli dari parent class (ListView) untuk mendapatkan konteks dasar.
        context = super().get_context_data(**kwargs)
        # Menambahkan 'title' ke konteks, yang bisa digunakan di template, misalnya untuk tag <title>.
        context['title'] = 'Kategori Buket'
        
        # Mengimpor 'defaultdict' dari library standar Python untuk mengelompokkan data dengan mudah.
        from collections import defaultdict
        # Membuat defaultdict, jika sebuah key belum ada, ia akan dibuat dengan nilai default berupa list kosong.
        semua_produk = defaultdict(list)
        # Melakukan loop untuk setiap objek 'p' (produk) di dalam tabel Produk.
        for p in Produk.objects.all():
            # Menambahkan produk 'p' ke dalam list yang ber-key 'p.kategori_id'. Ini mengelompokkan semua produk berdasarkan ID kategorinya.
            semua_produk[p.kategori_id].append(p)
        
        # Membuat sebuah list kosong untuk menampung struktur data akhir.
        daftar_kategori = []
        # Melakukan loop untuk setiap objek 'kategori' di dalam tabel Kategori.
        for kategori in Kategori.objects.all():
            # Mengambil daftar produk untuk kategori saat ini dari defaultdict 'semua_produk'. Jika tidak ada, kembalikan list kosong [].
            produk = semua_produk.get(kategori.id, [])
            # Menambahkan sebuah dictionary ke 'daftar_kategori'.
            daftar_kategori.append({
                'kategori': kategori, # Objek kategori itu sendiri.
                'produk': produk       # List produk yang termasuk dalam kategori ini.
            })

        # Menambahkan hasil pengelompokan tadi ke dalam konteks dengan nama 'product_list'.
        context['product_list'] = daftar_kategori
        # Mengembalikan konteks yang sudah lengkap untuk dirender oleh template.
        return context


class KategoriCreateview(LoginRequiredMixin, CreateView):
    """
    View untuk menampilkan form dan memproses pembuatan kategori baru.
    """
    # Menentukan template HTML yang berisi form untuk membuat kategori.
    template_name = 'admin/product/create_kategori.html'
    # Menentukan model yang akan dibuat objek barunya.
    model = Kategori
    # Menentukan form class yang akan digunakan.
    form_class = KategoriForm
    # URL tujuan jika form berhasil disubmit dan data valid. 'reverse_lazy' dipakai karena dievaluasi saat dibutuhkan.
    success_url = reverse_lazy('kategori')

    # Menambahkan data ke konteks.
    def get_context_data(self, **kwargs):
        # Memanggil method asli untuk mendapatkan konteks.
        context = super().get_context_data(**kwargs)
        # Menambahkan judul halaman.
        context['title'] = 'Tambah Kategori'
        # Mengembalikan konteks.
        return context
    
    # Method ini akan dijalankan jika data yang disubmit pada form tidak valid.
    def form_invalid(self, form):
        # Menambahkan pesan error umum ke dalam form.
        form.add_error(None, 'Periksa Kembali Inputan Anda')
        # Merender kembali halaman form (template_name) dengan data yang sudah diisi pengguna beserta pesan errornya.
        return render(self.request, self.template_name, {
            'form': form,
            'title': 'Tambah Kategori Gagal'
        })


class KategoriDeleteView(LoginRequiredMixin, DeleteView):
    """
    View untuk menghapus objek kategori. Dihapus langsung tanpa halaman konfirmasi.
    """
    # Menentukan model dari objek yang akan dihapus.
    model = Kategori
    # URL tujuan setelah objek berhasil dihapus.
    success_url = reverse_lazy('kategori')

    # Meng-override method 'get' agar penghapusan terjadi saat URL diakses dengan metode GET.
    def get(self, request, *args, **kwargs):
        # Mengambil objek Kategori berdasarkan 'pk' (primary key) dari URL.
        self.object = self.get_object()
        # Menghapus objek dari database.
        self.object.delete()
        # Mengalihkan pengguna ke URL yang didefinisikan di 'success_url'.
        return redirect(self.success_url)


class KategoriUpdateView(LoginRequiredMixin, UpdateView):
    """
    View untuk menampilkan form yang sudah terisi dan memproses pembaruan data kategori.
    """
    # Menentukan model yang akan di-update.
    model = Kategori
    # Menentukan form yang akan digunakan.
    form_class = KategoriForm
    # Menentukan file template yang berisi form update.
    template_name = 'admin/product/update_kategori.html'
    # URL tujuan setelah update berhasil.
    success_url = reverse_lazy('kategori')

    # Menambahkan data ke konteks.
    def get_context_data(self, **kwargs):
        # Memanggil method asli untuk mendapatkan konteks.
        context = super().get_context_data(**kwargs)
        # Menambahkan judul halaman.
        context['title'] = 'Update Kategori'
        # Mengembalikan konteks.
        return context