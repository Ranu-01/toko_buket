# --- IMPORTS ---

# Mixin ini digunakan untuk memastikan view hanya dapat diakses oleh pengguna yang sudah login.
from django.contrib.auth.mixins import LoginRequiredMixin
# Mengimpor Class-Based View (CBV) generik dari Django yang dirancang khusus untuk menampilkan daftar objek dari sebuah model.
from django.views.generic import ListView
# Mengimpor model 'Produk' dari file models.py yang berada di direktori induk (parent directory).
from ..models import Produk


# --- CLASS-BASED VIEW ---

# Mendefinisikan class view bernama HomeAllProdukView.
# LoginRequiredMixin: Aturan pertama, user harus login untuk mengakses halaman ini.
# ListView: Class ini akan menangani logika untuk mengambil daftar objek dari database dan mengirimkannya ke template.
class HomeAllProdukView(LoginRequiredMixin, ListView):
     # Menentukan model mana yang akan diambil datanya. Dalam hal ini, semua objek dari model 'Produk'.
     model = Produk
     # Menentukan file template HTML yang akan digunakan untuk menampilkan halaman ini.
     template_name = 'admin/index.html'
     # Mengganti nama variabel default ('object_list') di template menjadi 'semua_produk'.
     # Jadi, di dalam file index.html, Anda akan me-looping variabel 'semua_produk'.
     context_object_name = 'semua_produk'
     # Mengatur urutan data yang ditampilkan. Tanda '-' di depan 'id' berarti mengurutkan secara descending (dari yang terbesar ke terkecil),
     # efektif menampilkan produk yang baru ditambahkan di paling atas.
     ordering = ['-id']
     # Mengaktifkan paginasi (penomoran halaman) dan mengatur agar setiap halaman hanya menampilkan 10 produk.
     paginate_by = 10

     # Method ini digunakan untuk menambahkan data ekstra (konteks) yang akan dikirim ke template.
     def get_context_data(self, **kwargs):
          # Memanggil method asli dari parent class (ListView) untuk mendapatkan konteks dasar (yang sudah berisi 'semua_produk' dan info paginasi).
          context = super().get_context_data(**kwargs)
          
          # Menambahkan item baru ke dalam dictionary konteks. Variabel 'title' dengan nilai 'daftar produk' sekarang tersedia di template.
          context['title'] = 'daftar produk'
          # Mengembalikan dictionary konteks yang sudah dimodifikasi agar dapat digunakan saat merender template.
          return context