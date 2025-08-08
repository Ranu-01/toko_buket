from django import forms
from django.forms import modelformset_factory
from .models import Kategori,Produk,GambarProduk



class ProdukForm(forms.ModelForm):
     class Meta :
          model = Produk
          fields = ['nama',
                    'harga_normal',
                    'harga_promo',
                    'value_selling',
                    'deskripsi',
                    'value_isi_buket',
                    'kategori',
                    'slug'
                    ]
          
class KategoriForm(forms.ModelForm):
     class Meta :
          model = Kategori
          fields = ['nama']

class GambarProdukForm(forms.ModelForm):
     class Meta :
          model = GambarProduk
          fields = ['produk', 'gambar']

# Formset untuk banyak gambar
GambarProdukFormSet = modelformset_factory(
    GambarProduk,
    form=GambarProdukForm,
    extra=4  # jumlah form gambar yang muncul
)