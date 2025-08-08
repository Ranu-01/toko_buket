from django.db import models
from django.utils.text import slugify

class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama

class Produk(models.Model):
    nama = models.CharField(max_length=255)
    harga_normal = models.DecimalField(max_digits=10, decimal_places=2)
    harga_promo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    value_selling = models.CharField(max_length=255, help_text="Keunggulan/USP produk")
    deskripsi = models.TextField()
    value_isi_buket = models.TextField(help_text="Isi buket / item-item dalam produk")
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='produks')
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nama)
        super().save(*args, **kwargs)

class GambarProduk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='gambar_list')
    gambar = models.ImageField(upload_to='produk/')

    def __str__(self):
        return f"Gambar untuk {self.produk.nama}"
