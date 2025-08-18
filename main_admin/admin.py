# File: main_admin/admin.py

from django.contrib import admin
from .models import Kategori, Produk, GambarProduk

@admin.register(Kategori)
class KategoriAdmin(admin.ModelAdmin):
    """
    Menyesuaikan tampilan model Kategori di halaman admin.
    """
    list_display = ('nama',)
    search_fields = ('nama',)

class GambarProdukInline(admin.TabularInline):
    
    model = GambarProduk
    extra = 1  # Jumlah form kosong untuk upload gambar baru

@admin.register(Produk)
class ProdukAdmin(admin.ModelAdmin):
    
    # Menampilkan gambar produk secara inline di halaman edit produk
    inlines = [GambarProdukInline]
    
    # Kolom yang akan ditampilkan di halaman daftar produk
    list_display = ('nama', 'kategori', 'harga_normal', 'harga_promo', 'jumlah_dilihat')
    
    # Menambahkan filter berdasarkan kategori
    list_filter = ('kategori',)
    
    # Menambahkan fitur pencarian berdasarkan nama produk
    search_fields = ('nama',)
    
    # Membuat field ini hanya bisa dibaca (tidak bisa diedit manual)
    # karena slug di-generate otomatis dan jumlah_dilihat dihitung oleh view.
    readonly_fields = ('slug', 'jumlah_dilihat')

# Catatan: Kita tidak perlu mendaftarkan GambarProduk secara terpisah
# karena sudah ditampilkan secara inline di dalam ProdukAdmin.
