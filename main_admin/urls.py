
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (KategoriListView,KategoriCreateview,KategoriUpdateView,KategoriDeleteView,
                    ProductCreateView,DetailProdukView,AddProductImagesView,ProdukDeleteView,ProductListView,
                    HomeAllProdukView)
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path ('home/',HomeAllProdukView.as_view(),name='home'),
    
    path('list_produk',ProductListView.as_view(),name='list_produk'),
    path('create_produk/', ProductCreateView.as_view(), name='create_produk'),
    path('delete_produk/<int:pk>/', ProdukDeleteView.as_view(), name='delete_produk'),
    path('produk/<int:pk>/tambah-gambar/', AddProductImagesView.as_view(), name='add_product_images'),
    path('produk/detail/<int:pk>/', DetailProdukView.as_view(), name='detail_produk'),

    path ('kategori/',KategoriListView.as_view(),name='kategori'),
    path ('kategori_create/',KategoriCreateview.as_view(),name='create_kategori'),
    path ('kategori_update/<int:pk>/',KategoriUpdateView.as_view(),name='update_kategori'),
    path ('kategori_delete/<int:pk>/',KategoriDeleteView.as_view(),name='delete_kategori'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
