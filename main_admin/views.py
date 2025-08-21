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
from django.http import HttpResponseRedirect
from django.utils.text import slugify
import uuid
from django.contrib.auth.views import LoginView, LogoutView
from django.forms import modelformset_factory,inlineformset_factory
from django.urls import reverse_lazy, reverse
from .models import Kategori,GambarProduk,Produk
from .forms import KategoriForm,GambarProdukForm,ProdukForm,GambarProdukFormSet,RegistrasiAdminForm, LoginAdminForm
from django.db.models import Value, CharField,Q
from django.contrib.auth.mixins import LoginRequiredMixin


class KategoriListView(LoginRequiredMixin,ListView):
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
     
class KategoriCreateview(LoginRequiredMixin,CreateView):
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
     
class KategoriDeleteView(LoginRequiredMixin,DeleteView):
     model = Kategori
     success_url = reverse_lazy('kategori')

     def get(self,request,*args,**kwargs):
          self.object = self.get_object()
          self.object.delete()
          return redirect(self.success_url)
     
class KategoriUpdateView(LoginRequiredMixin,UpdateView):
     model = Kategori
     form_class = KategoriForm
     template_name = 'admin/product/update_kategori.html'
     success_url = reverse_lazy('kategori')

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context ['title'] = 'Update Kategori'
          return context


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
    

class AddProductImagesView(LoginRequiredMixin,View):
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
    

def edit_product_images(request, pk):
    """
    View berbasis fungsi untuk mengelola (tambah/ubah/hapus) gambar
    dari produk yang sudah ada.
    """
    produk = get_object_or_404(Produk, pk=pk)
    # Gunakan inlineformset_factory, yang lebih cocok untuk mengedit objek terkait
    ImageFormSet = inlineformset_factory(
        Produk, 
        GambarProduk, 
        form=GambarProdukForm, 
        extra=1, # Tampilkan 1 form kosong tambahan
        can_delete=True # Izinkan penghapusan gambar
    )

    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, instance=produk)
        if formset.is_valid():
            formset.save()
            # Redirect kembali ke halaman detail setelah berhasil
            return HttpResponseRedirect(reverse('detail_produk', kwargs={'pk': produk.pk}))
    else:
        formset = ImageFormSet(instance=produk)

    return render(request, 'admin/product/update_gambar.html', {
        'title': f'Edit Gambar untuk {produk.nama}',
        'produk': produk,
        'formset': formset
    })

    

class HomeAllProdukView(LoginRequiredMixin,ListView):
     model = Produk
     template_name = 'admin/index.html'
     context_object_name= 'semua_produk'
     ordering =['-id']
     paginate_by = 10

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          
          context['title'] = 'daftar produk'
          return context
     

     
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
    





class RegistrasiView(CreateView):
   
    form_class = RegistrasiAdminForm
    template_name = 'admin/auth/register.html'
    # Setelah registrasi berhasil, arahkan ke halaman login
    success_url = reverse_lazy('login_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrasi Admin Baru'
        return context

class LoginAdminView(LoginView):
 
    form_class = LoginAdminForm
    template_name = 'admin/auth/login.html'
    # Halaman yang akan dituju setelah login berhasil
    next_page = reverse_lazy('home') # Ganti 'home' dengan nama URL dashboard admin Anda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login Admin'
        return context

class LogoutAdminView(LogoutView):
    """
    View untuk menangani proses logout.
    """
    # Halaman yang akan dituju setelah logout berhasil
    next_page = reverse_lazy('login_admin')
