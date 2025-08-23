from ..models import Produk, GambarProduk
from django.views.generic import View
from django.shortcuts import render,get_object_or_404,redirect
from ..forms import GambarProduk,GambarProdukForm,GambarProdukFormSet
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse




class AddProductImagesView(LoginRequiredMixin,View):
    template_name = 'admin/product/add_gambar.html'

    def get(self, request, pk):
        # Ambil produk berdasarkan PK dari URL
        produk = get_object_or_404(Produk, pk=pk)
        
        # Siapkan formset kosong untuk di-render di template
        formset = GambarProdukFormSet(queryset=GambarProduk.objects.none())
        
        return render(request, self.template_name, {
            'title': f'Tambah Gambar untuk {produk.nama}',
            'produk': produk,
            'formset': formset
        })

    def post(self, request, pk):
        produk = get_object_or_404(Produk, pk=pk)
        
        # Proses data formset yang di-submit
        formset = GambarProdukFormSet(request.POST, request.FILES)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    # Ambil data dari form tapi jangan simpan dulu (commit=False)
                    gambar = form.save(commit=False)
                    # Kaitkan gambar dengan produk yang benar
                    gambar.produk = produk
                    gambar.save()
            # Setelah semua gambar disimpan, redirect ke daftar produk
            return redirect('list_produk')

        # Jika formset tidak valid, render kembali halaman dengan error
        return render(request, self.template_name, {
            'title': f'Tambah Gambar untuk {produk.nama}',
            'produk': produk,
            'formset': formset
        })
    

def edit_product_images(request, pk):
    """
    View berbasis fungsi untuk mengelola (tambah/ubah/hapus) gambar
    dari produk yang sudah ada.
    """
    produk = get_object_or_404(Produk, pk=pk)
    # Gunakan inlineformset_factory, yang lebih cocok untuk mengedit objek terkait
    ImageFormSet = inlineformset_factory(
        Produk, 
        GambarProduk, 
        form=GambarProdukForm, 
        extra=1, # Tampilkan 1 form kosong tambahan
        can_delete=True # Izinkan penghapusan gambar
    )

    if request.method == 'POST':
        formset = ImageFormSet(request.POST, request.FILES, instance=produk)
        if formset.is_valid():
            formset.save()
            # Redirect kembali ke halaman detail setelah berhasil
            return HttpResponseRedirect(reverse('detail_produk', kwargs={'pk': produk.pk}))
    else:
        formset = ImageFormSet(instance=produk)

    return render(request, 'admin/product/update_gambar.html', {
        'title': f'Edit Gambar untuk {produk.nama}',
        'produk': produk,
        'formset': formset
    })

    