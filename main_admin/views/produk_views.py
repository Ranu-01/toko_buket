# filename: views.py

# --- IMPORTS ---
# Digunakan untuk mengalihkan (redirect) pengguna ke URL lain setelah sebuah aksi selesai.
from django.shortcuts import redirect
# Mengimpor Class-Based Views (CBV) generik dari Django untuk operasi CRUD (Create, Read, Update, Delete) dan lainnya.
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView, DetailView
# 'reverse_lazy' dan 'reverse' digunakan untuk membuat URL berdasarkan nama URL yang didefinisikan di urls.py.
from django.urls import reverse_lazy, reverse
# 'Mixin' ini memastikan bahwa sebuah view hanya bisa diakses oleh pengguna yang sudah login.
from django.contrib.auth.mixins import LoginRequiredMixin
# 'Q' object digunakan untuk membangun query pencarian yang kompleks (misalnya, menggunakan logika OR).
from django.db.models import Q
# Mengimpor model 'Produk' dari file models.py di direktori yang sama.
from ..models import Produk
# Mengimpor form 'ProdukForm' dari file forms.py di direktori yang sama.
from ..forms import ProdukForm


# --- CLASS-BASED VIEWS ---

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    View untuk membuat (menambah) produk baru.
    """
    # Menentukan model mana yang akan digunakan untuk membuat objek baru.
    model = Produk
    # Menentukan form mana yang akan ditampilkan kepada pengguna.
    form_class = ProdukForm
    # Menentukan file template HTML yang akan dirender untuk halaman ini.
    template_name = 'admin/product/create.html'
    
    # Method ini digunakan untuk menambahkan data ekstra ke konteks yang akan dikirim ke template.
    def get_context_data(self, **kwargs):
        # Memanggil method asli dari parent class (CreateView) untuk mendapatkan konteks dasar.
        context = super().get_context_data(**kwargs)
        # Menambahkan variabel 'title' ke dalam konteks dengan nilai 'Tambah Detail Produk'.
        context['title'] = 'Tambah Detail Produk'
        # Mengembalikan konteks yang sudah dimodifikasi.
        return context

    # Method ini menentukan ke URL mana pengguna akan diarahkan setelah berhasil membuat produk.
    def get_success_url(self):
        # 'self.object' merujuk pada objek Produk yang baru saja dibuat.
        # reverse() akan membuat URL ke halaman 'add_product_images' dengan mengirimkan 'pk' (Primary Key) dari produk baru tersebut.
        return reverse('add_product_images', kwargs={'pk': self.object.pk})


class ProductListView(LoginRequiredMixin, ListView):
    """
    View untuk menampilkan daftar semua produk dengan fungsionalitas pencarian dan paginasi.
    """
    # Menentukan model yang akan didaftarkan.
    model = Produk
    # Menentukan file template HTML yang akan digunakan.
    template_name = 'admin/list_produk.html'
    # Mengganti nama variabel default 'object_list' di template menjadi 'produk_list'.
    context_object_name = 'produk_list'
    # Mengatur paginasi, hanya menampilkan 9 produk per halaman.
    paginate_by = 9

    # Method ini digunakan untuk memodifikasi query database dasar.
    def get_queryset(self):
        # Mengambil queryset dasar (semua objek Produk) dan mengurutkannya berdasarkan 'id' dari yang terbaru.
        queryset = super().get_queryset().order_by('-id')
        
        # Mengambil nilai parameter 'q' dari URL (misal: ?q=mawar). Jika tidak ada, nilainya 'None'.
        search_query = self.request.GET.get('q', None)
        
        # Jika ada query pencarian...
        if search_query:
            # ...filter queryset. Hanya tampilkan produk yang namanya ATAU deskripsinya mengandung kata kunci pencarian.
            queryset = queryset.filter(
                Q(nama__icontains=search_query) |
                Q(deskripsi__icontains=search_query)
            )
            
        # Mengembalikan queryset yang sudah difilter dan diurutkan.
        return queryset

    # Menambahkan data ekstra ke konteks.
    def get_context_data(self, **kwargs):
        # Mendapatkan konteks dari parent class.
        context = super().get_context_data(**kwargs)
        # Menambahkan judul halaman ke dalam konteks.
        context['title'] = 'Daftar Produk'
        # Menambahkan kata kunci pencarian ke konteks agar bisa ditampilkan kembali di input search.
        context['search_query'] = self.request.GET.get('q', '')
        # Mengembalikan konteks yang sudah dimodifikasi.
        return context


class DetailProdukView(LoginRequiredMixin, DetailView):
    """
    View untuk menampilkan detail satu objek produk.
    """
    # Menentukan model yang akan ditampilkan.
    model = Produk
    # Menentukan file template HTML yang akan digunakan.
    template_name = 'admin/detail_produk.html'
    # Mengganti nama default 'object' di template menjadi 'produk' agar lebih mudah dibaca.
    context_object_name = 'produk'

    # Menambahkan data ekstra ke konteks.
    def get_context_data(self, **kwargs):
        # Mendapatkan konteks dari parent class.
        context = super().get_context_data(**kwargs)
        # 'self.object' adalah objek Produk yang sedang ditampilkan.
        # Menambahkan judul halaman dinamis berdasarkan nama produk.
        context['title'] = self.object.nama
        # Mengembalikan konteks yang sudah dimodifikasi.
        return context


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    View untuk mengedit (memperbarui) produk yang sudah ada.
    """
    # Menentukan model yang akan diedit.
    model = Produk
    # Menentukan form yang akan digunakan.
    form_class = ProdukForm
    # Menentukan file template HTML yang akan digunakan.
    template_name = 'admin/product/update_produk.html'
    
    # Menambahkan data ekstra ke konteks.
    def get_context_data(self, **kwargs):
        # Mendapatkan konteks dari parent class.
        context = super().get_context_data(**kwargs)
        # Menambahkan judul halaman dinamis yang berisi nama produk yang sedang diedit.
        context['title'] = f'Edit Produk : {self.object.nama}'
        # Mengembalikan konteks.
        return context
    
    # Menentukan URL tujuan setelah produk berhasil di-update.
    def get_success_url(self):
        # Mengalihkan pengguna kembali ke halaman detail dari produk yang baru saja diedit.
        return reverse('detail_produk', kwargs={'pk': self.object.pk})


class ProdukDeleteView(LoginRequiredMixin, DeleteView):
    """
    View untuk menghapus produk secara langsung tanpa halaman konfirmasi.
    """
    # Menentukan model dari objek yang akan dihapus.
    model = Produk
    # URL tujuan setelah produk berhasil dihapus. 'reverse_lazy' digunakan karena URL dievaluasi saat server start.
    success_url = reverse_lazy('list_produk')

    # Kami meng-override method 'get' untuk menghapus objek secara langsung tanpa halaman konfirmasi.
    def get(self, request, *args, **kwargs):
        # 'self.get_object()' akan mengambil objek Produk berdasarkan 'pk' dari URL.
        self.object = self.get_object()
        # Menghapus objek dari database.
        self.object.delete()
        # Mengalihkan pengguna ke URL yang didefinisikan di 'success_url'.
        return redirect(self.success_url)