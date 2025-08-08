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
from django.urls import reverse_lazy
from .models import Kategori,GambarProduk,Produk
from .forms import KategoriForm,GambarProdukForm,ProdukForm
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
     success_url = reverse_lazy('admin/detail_kategori')

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
     success_url = reverse_lazy('admin/detail_kategori')

     def get(self,request,*args,**kwargs):
          self.object = self.get_object()
          self.object.delete()
          return redirect(self.success_url)
     
class KategoriUpdateView(UpdateView):
     model = Kategori
     form_class = KategoriForm
     template_name = 'admin/product/create_kategori.html'
     success_url = reverse_lazy('admin/detail_kategori')

     def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context ['title'] = 'Update Kategori'
          return context




def index(request):
     pass
     return render(request,'admin/index.html')


def detail(request):
     pass
     return render(request,'admin/detail.html')

def create(request):
     pass
     return render(request,'admin/product/create.html')
