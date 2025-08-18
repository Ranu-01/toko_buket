from django.urls import path,include
from . import views

app_name = 'customer'

urlpatterns = [
     path('', views.IndexView.as_view(), name='index'),
     path('kategori/', views.KategoriView.as_view(), name='kategori'),
     path('produk/<int:pk>/', views.ProductDetailView.as_view(), name='customer_product_detail'),

]