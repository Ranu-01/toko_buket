# File: main_admin/urls.py

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
# PERBAIKAN: Hapus impor yang panjang dan hanya gunakan satu baris ini
from . import views 

urlpatterns = [
    path('admin/', admin.site.urls),

    # PERBAIKAN: Panggil semua view menggunakan prefix 'views.'
    path('', views.HomeAllProdukView.as_view(), name='home'),
    
    path('list_produk', views.ProductListView.as_view(), name='list_produk'),
    path('create_produk/', views.ProductCreateView.as_view(), name='create_produk'),
    path('delete_produk/<int:pk>/', views.ProdukDeleteView.as_view(), name='delete_produk'),
    path('produk/detail/<int:pk>/', views.DetailProdukView.as_view(), name='detail_produk'),
    path('produk/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='edit_produk'),

    path('produk/<int:pk>/tambah-gambar/', views.AddProductImagesView.as_view(), name='add_product_images'),
    path('produk/edit-gambar/<int:pk>/', views.edit_product_images, name='edit_product_images'),

    path('kategori/', views.KategoriListView.as_view(), name='kategori'),
    path('kategori_create/', views.KategoriCreateview.as_view(), name='create_kategori'),
    path('kategori_update/<int:pk>/', views.KategoriUpdateView.as_view(), name='update_kategori'),
    path('kategori_delete/<int:pk>/', views.KategoriDeleteView.as_view(), name='delete_kategori'),

    # Ini sudah benar
    path('customer/', include('customer.urls')),

    path('register/', views.RegistrasiView.as_view(), name='register_admin'),
    path('login/', views.LoginAdminView.as_view(), name='login_admin'),
    path('logout/', views.LogoutAdminView.as_view(), name='logout_admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
