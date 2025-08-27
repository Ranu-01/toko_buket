# File: customer/views.py

# --- IMPORTS ---
# Mengimpor Class-Based Views (CBV) generik dari Django: ListView (untuk daftar), DetailView (untuk detail item), dan View (kelas dasar).
from django.views.generic import ListView, DetailView, View
# Mengimpor Q object untuk membuat query database yang kompleks (misalnya menggunakan logika OR).
from django.db.models import Q
# Mengimpor model Produk dan Kategori dari aplikasi 'main_admin'.
from main_admin.models import Produk, Kategori
# Mengimpor fungsi shortcut 'render' untuk merender template HTML.
from django.shortcuts import render

# --- CLASS-BASED VIEWS ---

class IndexView(ListView):
    """
    View untuk halaman utama (beranda) yang menampilkan daftar semua produk.
    """
    # Menentukan model yang akan ditampilkan datanya.
    model = Produk
    # Menentukan file template HTML yang akan digunakan.
    template_name = 'customer/index.html'
    # Mengganti nama variabel default 'object_list' di template menjadi 'semua_produk'.
    context_object_name = 'semua_produk'
    # Mengaktifkan paginasi, menampilkan 12 produk per halaman.
    paginate_by = 12

    # Method ini untuk memodifikasi query dasar yang mengambil data dari model.
    def get_queryset(self):
        # Mengambil queryset default (semua produk) dan mengurutkannya dari yang terbaru (-id).
        queryset = super().get_queryset().order_by('-id')
        # Mengambil nilai parameter 'q' dari URL (misal: /?q=bunga). Jika tidak ada, nilainya None.
        search_query = self.request.GET.get('q', None)
        
        # Jika ada kata kunci pencarian...
        if search_query:
            # ...filter queryset. Tampilkan produk yang namanya ATAU nama kategorinya mengandung kata kunci.
            queryset = queryset.filter(
                Q(nama__icontains=search_query) |
                Q(kategori__nama__icontains=search_query) # __icontains = case-insensitive contains
            )
        # Mengembalikan queryset yang sudah diurutkan dan difilter.
        return queryset

    # Method ini untuk menambahkan data ekstra (konteks) ke template.
    def get_context_data(self, **kwargs):
        # Memanggil method asli untuk mendapatkan konteks dasar (sudah berisi 'semua_produk' dan info paginasi).
        context = super().get_context_data(**kwargs)
        # Menambahkan judul halaman.
        context['title'] = 'Beranda'
        # Mengirim kembali kata kunci pencarian ke template, agar bisa ditampilkan lagi di kotak search.
        context['search_query'] = self.request.GET.get('q', '')
        
        # Mengambil semua objek Kategori dari database.
        semua_kategori = Kategori.objects.all()
        # Membuat list kosong untuk menampung kategori yang memiliki produk.
        kategori_dengan_produk = []

        # Melakukan iterasi untuk setiap objek kategori.
        for kategori in semua_kategori:
            # Untuk setiap kategori, ambil 4 produk terbarunya. 'produks' adalah related_name dari ForeignKey di model Produk.
            produk_terbaru = kategori.produks.order_by('-id')[:4]
            # Cek apakah queryset 'produk_terbaru' tidak kosong.
            if produk_terbaru.exists():
                # Jika ada produk, tambahkan dictionary berisi nama kategori dan daftar produknya ke list.
                kategori_dengan_produk.append({
                    'nama': kategori.nama,
                    'produks': produk_terbaru
                })
        
        # Menambahkan list kategori yang sudah diolah ke dalam konteks.
        context['kategori_list'] = kategori_dengan_produk
        
        # Mengembalikan konteks akhir ke template.
        return context

class KategoriView(ListView):
    """
    View untuk halaman kategori. Logikanya sangat mirip dengan IndexView.
    Perbedaan utama biasanya terletak pada template atau cara data disajikan.
    """
    model = Produk
    template_name = 'customer/kategori.html'
    context_object_name = 'semua_produk'
    paginate_by = 12

    # Method get_queryset identik dengan IndexView untuk fungsionalitas pencarian.
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        search_query = self.request.GET.get('q', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(nama__icontains=search_query) |
                Q(kategori__nama__icontains=search_query)
            )
        return queryset

    # Method get_context_data juga identik dengan IndexView untuk menampilkan daftar kategori beserta produknya.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Kategori' # Mungkin judulnya bisa diubah agar sesuai.
        context['search_query'] = self.request.GET.get('q', '')
        
        semua_kategori = Kategori.objects.all()
        kategori_dengan_produk = []

        for kategori in semua_kategori:
            produk_terbaru = kategori.produks.order_by('-id')[:4]
            if produk_terbaru.exists():
                kategori_dengan_produk.append({
                    'nama': kategori.nama,
                    'produks': produk_terbaru
                })
        
        context['kategori_list'] = kategori_dengan_produk
        return context

class ProductDetailView(DetailView):
    """
    View untuk menampilkan halaman detail dari satu produk.
    """
    model = Produk
    template_name = 'customer/detail_produk.html'
    # Nama variabel di template untuk objek produk yang sedang ditampilkan.
    context_object_name = 'produk'

    # Menambahkan data ekstra ke template.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'self.object' adalah cara untuk mengakses objek produk yang sedang ditampilkan di DetailView.
        current_product = self.object
        
        # 1. Menambahkan 1 ke penghitung jumlah dilihat setiap kali halaman ini diakses.
        current_product.jumlah_dilihat += 1
        # Menyimpan perubahan hanya pada field 'jumlah_dilihat' agar lebih efisien.
        current_product.save(update_fields=['jumlah_dilihat'])
        
        # Mengatur judul halaman secara dinamis berdasarkan nama produk.
        context['title'] = f"Detail: {current_product.nama}"
        
        # 2. Mengambil produk terkait: produk lain dari kategori yang sama.
        related_products = Produk.objects.filter(
            kategori=current_product.kategori  # Filter berdasarkan kategori yang sama.
        ).exclude(
            pk=current_product.pk  # Kecualikan produk yang sedang dilihat saat ini.
        ).order_by('-id')[:4]  # Urutkan dari yang terbaru dan ambil 4 produk.
        
        # Menambahkan produk terkait ke konteks.
        context['related_products'] = related_products
        
        # 3. Mengambil 4 produk terpopuler (paling banyak dilihat) dari seluruh toko.
        popular_products = Produk.objects.order_by(
            '-jumlah_dilihat'  # Urutkan berdasarkan jumlah dilihat (descending).
        ).exclude(
            pk=current_product.pk # Kecualikan produk yang sedang dilihat.
        )[:4] # Ambil 4 teratas.
        
        # Menambahkan produk populer ke konteks.
        context['popular_products'] = popular_products
        
        # Mengembalikan konteks akhir.
        return context

class AboutView(View):
    """
    View sederhana untuk menampilkan halaman statis 'Tentang Kami'.
    """
    # Method ini menangani HTTP GET request.
    def get(self, request):
        # Membuat dictionary konteks secara manual.
        context = {
            'title': 'Tentang Kami'
        }
        # Merender template dengan konteks yang diberikan.
        return render(request, 'customer/about_me.html', context)

class contactView(View):
    """
    View sederhana untuk menampilkan halaman statis 'Kontak'.
    """
    # Method ini menangani HTTP GET request.
    def get(self, request):
        # Membuat dictionary konteks.
        context = {
            'title': 'Contact'
        }
        # Merender template dengan konteks.
        return render(request, 'customer/contact.html', context)