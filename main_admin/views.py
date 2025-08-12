from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.views.generic import (
     ListView,
     View,
     CreateView,
     DeleteView,
     UpdateView,
     DetailView,
     RedirectView,
     TemplateView
     )
from django.utils.text import slugify
import uuid
from django.forms import modelformset_factory
from django.urls import reverse_lazy, reverse
from .models import Kategori,GambarProduk,Produk
from .forms import KategoriForm,GambarProdukForm,ProdukForm,GambarProdukFormSet
from django.db.models import Value, CharField,Q


class KategoriListView(ListView):
     model = Kategori
     template_name = 'admin/detail_kategori.html'
     context_object_name = 'semua_kategori'

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['title'] ='Kategori Buket'
          from collections import defaultdict
          semua_produk = defaultdict(list)
          for p in Produk.objects.all():
               semua_produk[p.kategori_id].append(p)
          daftar_kategori = []
          for kategori in Kategori.objects.all():
               produk = semua_produk.get(kategori.id,[])
               daftar_kategori.append({
                    'kategori': kategori,
                    'produk' : produk
               })

          context['product_list'] = daftar_kategori
          return context
     
class KategoriCreateview(CreateView):
     template_name = 'admin/product/create_kategori.html'
     model = Kategori
     form_class = KategoriForm
     success_url = reverse_lazy('kategori')

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['title'] = 'Tambah Kategori'
          return context
     
     def form_invalid(self, form):
          form.add_error(None, 'Periksa Kembali Inputan Anda')

          return render  (self.request, self.template_name,{
               'form' : form,
               'title' : 'Tamabah Kategori Gagal'
          })
     
class KategoriDeleteView(DeleteView):
     model = Kategori
     success_url = reverse_lazy('kategori')

     def get(self,request,*args,**kwargs):
          self.object = self.get_object()
          self.object.delete()
          return redirect(self.success_url)
     
class KategoriUpdateView(UpdateView):
     model = Kategori
     form_class = KategoriForm
     template_name = 'admin/product/update_kategori.html'
     success_url = reverse_lazy('kategori')

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context ['title'] = 'Update Kategori'
          return context


class ProductCreateView(CreateView):
    model = Produk
    form_class = ProdukForm
    template_name = 'admin/product/create.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tambah Detail Produk'
        return context

    def get_success_url(self):
        
        return reverse('add_product_images', kwargs={'pk': self.object.pk})
    

class AddProductImagesView(View):
    template_name = 'admin/product/add_gambar.html'

    def get(self, request, pk):
        # Ambil produk berdasarkan PK dari URL
        produk = get_object_or_404(Produk, pk=pk)
        
        # Siapkan formset kosong untuk di-render di template
        formset = GambarProdukFormSet(queryset=GambarProduk.objects.none())
        
        return render(request, self.template_name, {
            'title': f'Tambah Gambar untuk {produk.nama}',
            'produk': produk,
            'formset': formset
        })

    def post(self, request, pk):
        produk = get_object_or_404(Produk, pk=pk)
        
        # Proses data formset yang di-submit
        formset = GambarProdukFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    # Ambil data dari form tapi jangan simpan dulu (commit=False)
                    gambar = form.save(commit=False)
                    # Kaitkan gambar dengan produk yang benar
                    gambar.produk = produk
                    gambar.save()
            # Setelah semua gambar disimpan, redirect ke daftar produk
            return redirect('list_produk')

        # Jika formset tidak valid, render kembali halaman dengan error
        return render(request, self.template_name, {
            'title': f'Tambah Gambar untuk {produk.nama}',
            'produk': produk,
            'formset': formset
        })
    
    

class HomeAllProdukView(ListView):
     model = Produk
     template_name = 'admin/index.html'
     context_object_name= 'semua_produk'
     ordering =['-id']
     paginate_by = 10

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          
          context['title'] = 'daftar produk'
          return context
     

class DetailProdukView(DetailView):
    model = Produk  # model yang mau ditampilkan
    template_name = 'admin/detail_produk.html'  # template untuk menampilkan data
    context_object_name = 'produk'      
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     context['title'] = 'Daftar Produk'
     return context

     
class ProdukDeleteView(DeleteView):
     model = Produk
     success_url = reverse_lazy('list_produk')

     def get(self,request,*args,**kwargs):
          self.object = self.get_object()
          self.object.delete()
          return redirect(self.success_url)
     
class ProductListView(ListView):
   
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
    


