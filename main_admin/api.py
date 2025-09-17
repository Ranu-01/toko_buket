# katalog_app/api.py
from rest_framework import viewsets
from .models import Kategori, Produk
from .serializers import KategoriSerializer, ProdukSerializer

class KategoriViewSet(viewsets.ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer

class ProdukViewSet(viewsets.ModelViewSet):
    queryset = Produk.objects.all()
    serializer_class = ProdukSerializer
    lookup_field = 'slug'