
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from .views import (KategoriListView,KategoriCreateview,KategoriUpdateView,KategoriDeleteView,
                    ProductCreateView,DetailProdukView,AddProductImagesView,ProdukDeleteView,ProductListView,ProductUpdateView,
                    HomeAllProdukView,
                    RegistrasiView, LoginAdminView, LogoutAdminView)
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path ('',HomeAllProdukView.as_view(),name='home'),
    
    path('list_produk',ProductListView.as_view(),name='list_produk'),
    path('create_produk/', ProductCreateView.as_view(), name='create_produk'),
    path('delete_produk/<int:pk>/', ProdukDeleteView.as_view(), name='delete_produk'),
    path('produk/<int:pk>/tambah-gambar/', AddProductImagesView.as_view(), name='add_product_images'),
    path('produk/detail/<int:pk>/', DetailProdukView.as_view(), name='detail_produk'),
    path('produk/edit/<int:pk>/', ProductUpdateView.as_view(), name='edit_produk'),

    path ('kategori/',KategoriListView.as_view(),name='kategori'),
    path ('kategori_create/',KategoriCreateview.as_view(),name='create_kategori'),
    path ('kategori_update/<int:pk>/',KategoriUpdateView.as_view(),name='update_kategori'),
    path ('kategori_delete/<int:pk>/',KategoriDeleteView.as_view(),name='delete_kategori'),


    path ('customer/',include('customer.urls', namespace='customer')),


    path('register/', RegistrasiView.as_view(), name='register_admin'),
    path('login/', LoginAdminView.as_view(), name='login_admin'),
    path('logout/', LogoutAdminView.as_view(), name='logout_admin'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
