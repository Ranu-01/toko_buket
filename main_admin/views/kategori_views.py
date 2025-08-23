from django.shortcuts import render,redirect
from django.views.generic import ListView,CreateView,DeleteView,UpdateView
from django.urls import reverse_lazy, reverse
from ..models import Kategori, Produk
from django.contrib.auth.mixins import LoginRequiredMixin
from ..forms import Kategori,Produk,KategoriForm



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
