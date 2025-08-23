from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from ..models import Produk




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
     
