# my_app/serializers.py
from rest_framework import serializers
from .models import Kategori, Produk, GambarProduk

# Serializer untuk GambarProduk
class GambarProdukSerializer(serializers.ModelSerializer):
    class Meta:
        model = GambarProduk
        fields = ['gambar']

# Serializer untuk Produk
class ProdukSerializer(serializers.ModelSerializer):
    # Field untuk menampilkan gambar-gambar terkait produk
    gambar_list = GambarProdukSerializer(many=True, read_only=True)
    kategori_nama = serializers.CharField(source='kategori.nama', read_only=True)

    class Meta:
        model = Produk
        fields = [
            'id', 'nama', 'harga_normal', 'harga_promo', 'value_selling', 
            'deskripsi', 'value_isi_buket', 'kategori', 'kategori_nama', 
            'slug', 'jumlah_dilihat', 'gambar_list'
        ]

# Serializer untuk Kategori
class KategoriSerializer(serializers.ModelSerializer):
    # Menampilkan daftar produk yang terkait dengan kategori ini
    produks = ProdukSerializer(many=True, read_only=True)

    class Meta:
        model = Kategori
        fields = ['id', 'nama', 'produks']