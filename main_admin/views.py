from django.shortcuts import render,redirect,get_list_or_404,get_object_or_404
from django.views.generic import (
     ListView,
     View,
     CreateView,
     DeleteView,
     UpdateView,
     RedirectView,
     TemplateView
     )
from django.utils.text import slugify
import uuid
from django.forms import modelformset_factory
from django.urls import reverse_lazy
from .models import Kategori,GambarProduk,Produk
from .forms import KategoriForm,GambarProdukForm,ProdukForm,GambarProdukFormSet
from django.db.models import Value, CharField


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


class ProductCreateView(View):
    template_name = 'admin/product/create.html'

    def get(self, request):
        kategori_list = Kategori.objects.all()  # untuk dropdown kategori di form
        return render(request, self.template_name, {
            'kategori_list': kategori_list
        })

    def post(self, request):
        # Ambil data dari form HTML manual
        nama = request.POST.get('nama')
        harga_normal = request.POST.get('harga_normal')
        harga_promo = request.POST.get('harga_promo') or None
        value_selling = request.POST.get('value_selling')
        deskripsi = request.POST.get('deskripsi')
        value_isi_buket = request.POST.get('value_isi_buket')
        kategori_id = request.POST.get('kategori')

        kategori = Kategori.objects.get(id=kategori_id)

        # Simpan produk
        produk = Produk.objects.create(
            nama=nama,
            harga_normal=harga_normal,
            harga_promo=harga_promo,
            value_selling=value_selling,
            deskripsi=deskripsi,
            value_isi_buket=value_isi_buket,
            kategori=kategori
            # slug akan otomatis di-generate di method save()
        )

        # Ambil semua file gambar (name="gambar" di HTML harus multiple)
        gambar_files = request.FILES.getlist('gambar')

        for file in gambar_files:
            GambarProduk.objects.create(
                produk=produk,
                gambar=file
            )

        return redirect('index')  # ganti dengan url tujuan setelah sukses

class ProductListView(ListView):
    model = Produk  # model yang mau ditampilkan
    template_name = 'admin/detail.html'  # template untuk menampilkan data
    context_object_name = 'produk_list'  # nama variabel di template
    ordering = ['-id']  # urutkan dari terbaru
    paginate_by = 10  # kalau mau pagination

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Daftar Produk'
        return context
