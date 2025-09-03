from django.db import models
from django.utils.text import slugify


class Kategori(models.Model):
    nama = models.CharField(max_length=100)
    
    def __str__(self):
        return self.nama

class Produk(models.Model):
    nama = models.CharField(max_length=255)
    harga_normal = models.DecimalField(max_digits=15, decimal_places=0)
    harga_promo = models.DecimalField(max_digits=15, decimal_places=0, blank=True, null=True)
    value_selling = models.CharField(max_length=255, help_text="Keunggulan/USP produk", blank=True, null=True)
    deskripsi = models.TextField(blank=True, null=True)
    value_isi_buket = models.TextField(help_text="Isi buket / item-item dalam produk", blank=True, null=True)
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE, related_name='produks')
    slug = models.SlugField(unique=True, blank=True)
    jumlah_dilihat = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nama

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_candidate = slugify(self.nama)
            unique_slug = slug_candidate
            counter = 1
            while Produk.objects.filter(slug=unique_slug).exists():
                unique_slug = f'{slug_candidate}-{counter}'
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

class GambarProduk(models.Model):
    produk = models.ForeignKey(Produk, on_delete=models.CASCADE, related_name='gambar_list')
    gambar = models.ImageField(upload_to='produk/')

    def __str__(self):
        return f"Gambar untuk {self.produk.nama}"
