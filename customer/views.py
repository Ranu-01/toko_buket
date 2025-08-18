# File: customer/views.py

from django.views.generic import ListView,DetailView
from django.db.models import Q
from main_admin.models import Produk, Kategori 

class IndexView(ListView):
    model = Produk
    template_name = 'customer/index.html'
    context_object_name = 'semua_produk'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        search_query = self.request.GET.get('q', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(nama__icontains=search_query) |
                Q(kategori__nama__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Beranda'
        context['search_query'] = self.request.GET.get('q', '')
        
        semua_kategori = Kategori.objects.all()
        kategori_dengan_produk = []

        for kategori in semua_kategori:
            # Ambil 4 produk terbaru untuk kategori ini
            produk_terbaru = kategori.produks.order_by('-id')[:4]
            # Tambahkan ke daftar jika kategori ini punya produk
            if produk_terbaru.exists():
                kategori_dengan_produk.append({
                    'nama': kategori.nama,
                    'produks': produk_terbaru
                })
        
        context['kategori_list'] = kategori_dengan_produk
        
        return context
    
class KategoriView(ListView):
    model = Produk
    template_name = 'customer/kategori.html'
    context_object_name = 'semua_produk'
    paginate_by = 12

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-id')
        search_query = self.request.GET.get('q', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(nama__icontains=search_query) |
                Q(kategori__nama__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['title'] = 'Beranda'
        context['search_query'] = self.request.GET.get('q', '')
        
        semua_kategori = Kategori.objects.all()
        kategori_dengan_produk = []

        for kategori in semua_kategori:
            # Ambil 4 produk terbaru untuk kategori ini
            produk_terbaru = kategori.produks.order_by('-id')[:4]
            # Tambahkan ke daftar jika kategori ini punya produk
            if produk_terbaru.exists():
                kategori_dengan_produk.append({
                    'nama': kategori.nama,
                    'produks': produk_terbaru
                })
        
        context['kategori_list'] = kategori_dengan_produk
        
        return context
class ProductDetailView(DetailView):
    model = Produk
    template_name = 'customer/detail_produk.html'
    context_object_name = 'produk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_product = self.object
        
        # 1. Tambahkan 1 ke penghitung setiap kali halaman dilihat
        current_product.jumlah_dilihat += 1
        current_product.save(update_fields=['jumlah_dilihat']) # Lebih efisien
        
        context['title'] = f"Detail: {current_product.nama}"
        
        # 2. Ambil produk terkait dari kategori yang sama (sudah ada)
        related_products = Produk.objects.filter(
            kategori=current_product.kategori
        ).exclude(
            pk=current_product.pk
        ).order_by('-id')[:4]
        
        context['related_products'] = related_products
        
        # 3. TAMBAHAN: Ambil 4 produk terpopuler dari seluruh toko
        popular_products = Produk.objects.order_by(
            '-jumlah_dilihat'
        ).exclude(
            pk=current_product.pk
        )[:4]
        
        context['popular_products'] = popular_products
        
        return context
