from django import forms
from django.forms import modelformset_factory
from .models import Kategori,Produk,GambarProduk


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        exclude = ['slug'] # Slug di-generate otomatis, jadi kita kecualikan
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Produk'}),
            'harga_normal': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Contoh: 150000'}),
            'harga_promo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Boleh kosong'}),
            'value_selling': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Keunggulan/USP produk'}),
            'deskripsi': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Deskripsi lengkap produk'}),
            'value_isi_buket': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Contoh: 10x Mawar Merah, 1x Boneka'}),
            'kategori': forms.Select(attrs={'class': 'form-control select2'}),
        }
          
class KategoriForm(forms.ModelForm):
     class Meta :
          model = Kategori
          fields = ['nama']

class GambarProdukForm(forms.ModelForm):
     class Meta :
          model = GambarProduk
          fields = [ 'gambar']

# Formset untuk banyak gambar
GambarProdukFormSet = modelformset_factory(
    GambarProduk,
    form=GambarProdukForm,
    extra=4  # jumlah form gambar yang muncul
)