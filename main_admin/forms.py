from django import forms
from django.forms import modelformset_factory
from .models import Kategori,Produk,GambarProduk
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class ProdukForm(forms.ModelForm):
    class Meta:
        model = Produk
        exclude = ['slug','jumlah_dilihat'] # Slug di-generate otomatis, jadi kita kecualikan
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



# untuk regristasi dan login

class RegistrasiAdminForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tambahkan perulangan ini untuk menerapkan class ke semua field
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'Masukkan {field.label.lower()}'

class LoginAdminForm(AuthenticationForm):
    """
    Form untuk login admin.
    Mewarisi dari AuthenticationForm yang secara khusus dirancang untuk login.
    """
    # Kita bisa menambahkan atribut CSS di sini agar sesuai dengan template
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))
