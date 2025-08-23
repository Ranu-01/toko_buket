from django.shortcuts import redirect
from django.views.generic import ListView, View, CreateView, DeleteView, UpdateView, DetailView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from ..models import Produk
from ..forms import ProdukForm





class ProductCreateView(LoginRequiredMixin,CreateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'admin/product/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Detail Produk'
        return context

    def get_success_url(self):
        
        return reverse('add_product_images', kwargs={'pk': self.object.pk})
    
     
class ProdukDeleteView(LoginRequiredMixin,DeleteView):
     model = Produk
     success_url = reverse_lazy('list_produk')

     def get(self,request,*args,**kwargs):
          self.object = self.get_object()
          self.object.delete()
          return redirect(self.success_url)
     

class DetailProdukView(LoginRequiredMixin,DetailView):
   
    model = Produk
    template_name = 'admin/detail_produk.html'
    # Nama variabel di template adalah 'produk' (tunggal)
    context_object_name = 'produk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'self.object' adalah produk yang sedang ditampilkan
        context['title'] = self.object.nama
        return context
    
    
     
class ProductListView(LoginRequiredMixin,ListView):
   
    model = Produk
    # Ganti 'product/product_list.html' dengan path template Anda yang sebenarnya.
    template_name = 'admin/list_produk.html'
    # Nama variabel yang akan digunakan di dalam template untuk menampung daftar produk.
    context_object_name = 'produk_list'
    # Jumlah produk yang ditampilkan per halaman.
    paginate_by = 9

    def get_queryset(self):
        # Ambil queryset dasar (semua produk) dan urutkan dari yang terbaru.
        queryset = super().get_queryset().order_by('-id')
        
        # Ambil keyword pencarian dari parameter URL (misal: /produk/?q=mawar).
        search_query = self.request.GET.get('q', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(nama__icontains=search_query) |
                Q(deskripsi__icontains=search_query)
            )
            
        return queryset

    def get_context_data(self, **kwargs):
        # Panggil implementasi dasar terlebih dahulu untuk mendapatkan konteks.
        context = super().get_context_data(**kwargs)
        
        # Tambahkan judul halaman ke dalam konteks.
        context['title'] = 'Daftar Produk'
        context['search_query'] = self.request.GET.get('q', '')
        
        return context
    

class ProductUpdateView(LoginRequiredMixin,UpdateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'admin/product/update_produk.html'
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context ['title'] = f'Edit Produk : {self.object.nama}'
        return context
    
    def get_success_url(self):
        return reverse('detail_produk',kwargs={'pk' : self.object.pk})
    
