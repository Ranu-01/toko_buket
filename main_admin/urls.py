"""
URL configuration for admin project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import (KategoriListView,KategoriCreateview,KategoriUpdateView,KategoriDeleteView,
                    ProductCreateView,ProductListView,AddProductImagesView)
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('produk/', ProductListView.as_view(), name='product_list'),
    path('create_produk/', ProductCreateView.as_view(), name='create_produk'),
    path('produk/<int:pk>/tambah-gambar/', AddProductImagesView.as_view(), name='add_product_images'),

    path ('kategori/',KategoriListView.as_view(),name='kategori'),
    path ('kategori_create/',KategoriCreateview.as_view(),name='create_kategori'),
    path ('kategori_update/<int:pk>/',KategoriUpdateView.as_view(),name='update_kategori'),
    path ('kategori_delete/<int:pk>/',KategoriDeleteView.as_view(),name='delete_kategori'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
