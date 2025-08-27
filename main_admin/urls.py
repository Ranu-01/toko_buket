# File: main_admin/urls.py

# --- IMPORTS ---

# Mengimpor situs admin bawaan dari Django.
from django.contrib import admin
# Mengimpor file settings.py dari proyek Anda untuk mengakses konfigurasi seperti DEBUG, MEDIA_URL, dll.
from django.conf import settings
# Mengimpor fungsi helper untuk menyajikan file statis (seperti media) selama mode development.
from django.conf.urls.static import static
# Mengimpor 'path' untuk mendefinisikan setiap rute URL dan 'include' untuk menyertakan file URL dari aplikasi lain.
from django.urls import path, include
# Mengimpor file views.py dari direktori yang sama (main_admin) agar bisa memanggil semua view dari sana.
from . import views 

# 'urlpatterns' adalah sebuah list yang Django cari untuk melakukan routing URL.
urlpatterns = [
    # Rute untuk mengakses halaman admin bawaan Django.
    path('admin/', admin.site.urls),

    # --- URL APLIKASI UTAMA ---
    # Rute untuk halaman utama/dashboard admin. Menggunakan 'as_view()' karena ini adalah Class-Based View.
    path('', views.HomeAllProdukView.as_view(), name='home'),
    
    # --- URL UNTUK MANAJEMEN PRODUK ---
    # Halaman untuk menampilkan daftar semua produk.
    path('list_produk', views.ProductListView.as_view(), name='list_produk'),
    # Halaman untuk menampilkan form pembuatan produk baru.
    path('create_produk/', views.ProductCreateView.as_view(), name='create_produk'),
    # URL untuk menghapus produk. '<int:pk>' menangkap angka dari URL dan meneruskannya sebagai argumen 'pk' ke view.
    path('delete_produk/<int:pk>/', views.ProdukDeleteView.as_view(), name='delete_produk'),
    # Halaman untuk melihat detail satu produk berdasarkan 'pk' (primary key).
    path('produk/detail/<int:pk>/', views.DetailProdukView.as_view(), name='detail_produk'),
    # Halaman untuk mengedit produk yang sudah ada berdasarkan 'pk'.
    path('produk/edit/<int:pk>/', views.ProductUpdateView.as_view(), name='edit_produk'),

    # --- URL UNTUK MANAJEMEN GAMBAR PRODUK ---
    # Halaman untuk menambah gambar ke produk tertentu.
    path('produk/<int:pk>/tambah-gambar/', views.AddProductImagesView.as_view(), name='add_product_images'),
    # Halaman untuk mengedit gambar yang sudah ada pada produk tertentu. Ini adalah Function-Based View, jadi tidak pakai '.as_view()'.
    path('produk/edit-gambar/<int:pk>/', views.edit_product_images, name='edit_product_images'),

    # --- URL UNTUK MANAJEMEN KATEGORI ---
    # Halaman untuk menampilkan daftar kategori.
    path('kategori/', views.KategoriListView.as_view(), name='kategori'),
    # Halaman untuk membuat kategori baru.
    path('kategori_create/', views.KategoriCreateview.as_view(), name='create_kategori'),
    # Halaman untuk memperbarui kategori berdasarkan 'pk'.
    path('kategori_update/<int:pk>/', views.KategoriUpdateView.as_view(), name='update_kategori'),
    # URL untuk menghapus kategori berdasarkan 'pk'.
    path('kategori_delete/<int:pk>/', views.KategoriDeleteView.as_view(), name='delete_kategori'),

    # --- URL INKLUSI APLIKASI LAIN ---
    # Mendelegasikan semua URL yang berawalan 'customer/' untuk ditangani oleh file 'urls.py' di dalam aplikasi 'customer'.
    path('customer/', include('customer.urls')),

    # --- URL UNTUK AUTENTIKASI ADMIN ---
    # Halaman registrasi untuk admin baru.
    path('register/', views.RegistrasiView.as_view(), name='register_admin'),
    # Halaman login untuk admin.
    path('login/', views.LoginAdminView.as_view(), name='login_admin'),
    # URL untuk proses logout.
    path('logout/', views.LogoutAdminView.as_view(), name='logout_admin'),
]

# --- KONFIGURASI FILE MEDIA (HANYA UNTUK DEVELOPMENT) ---
# Cek apakah proyek berjalan dalam mode DEBUG (pengembangan).
if settings.DEBUG:
    # Jika ya, tambahkan URL pattern khusus untuk menyajikan file yang di-upload pengguna (media files).
    # Ini memungkinkan gambar yang Anda upload bisa tampil di browser selama pengembangan.
    # CATATAN: Ini tidak boleh digunakan di lingkungan produksi (production).
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)