# --- IMPORTS ---

# Mengimpor Class-Based View (CBV) generik dari Django yang khusus untuk menangani pembuatan objek baru melalui form.
from django.views.generic import CreateView
# Mengimpor dua class form kustom: 'RegistrasiAdminForm' untuk registrasi dan 'LoginAdminForm' untuk login.
from ..forms import RegistrasiAdminForm, LoginAdminForm
# Mengimpor fungsi 'reverse_lazy' untuk membuat URL dari nama URL pattern. '_lazy' berarti URL baru akan dievaluasi saat dibutuhkan, cocok untuk atribut level kelas.
from django.urls import reverse_lazy
# Mengimpor view bawaan Django yang sudah siap pakai untuk menangani proses login dan logout pengguna.
from django.contrib.auth.views import LoginView, LogoutView


# --- CLASS-BASED VIEWS UNTUK AUTENTIKASI ---

class RegistrasiView(CreateView):
    """
    View untuk menangani halaman registrasi admin baru.
    Menggunakan CreateView karena registrasi pada dasarnya adalah membuat objek 'User' baru.
    """
    # Menentukan class form mana yang akan digunakan untuk validasi dan rendering di template.
    form_class = RegistrasiAdminForm
    # Menentukan file template HTML yang akan ditampilkan untuk halaman registrasi ini.
    template_name = 'admin/auth/register.html'
    # Menentukan URL tujuan (redirect) jika proses registrasi (form submission) berhasil dan valid.
    success_url = reverse_lazy('login_admin')

    # Method ini digunakan untuk menambahkan data tambahan ke konteks yang akan dikirim ke template.
    def get_context_data(self, **kwargs):
        # Memanggil method asli dari parent class (CreateView) untuk mendapatkan konteks dasar.
        context = super().get_context_data(**kwargs)
        # Menambahkan variabel 'title' ke dalam konteks dengan nilai 'Registrasi Admin Baru'.
        context['title'] = 'Registrasi Admin Baru'
        # Mengembalikan konteks yang sudah dimodifikasi.
        return context


class LoginAdminView(LoginView):
    """
    View untuk menangani halaman login admin.
    Mewarisi fungsionalitas dari LoginView bawaan Django, jadi kita hanya perlu mengkonfigurasinya.
    """
    # Menentukan class form mana yang akan digunakan, dalam hal ini form login kustom kita.
    form_class = LoginAdminForm
    # Menentukan file template HTML yang akan menampilkan form login.
    template_name = 'admin/auth/login.html'
    # Menentukan URL tujuan (redirect) jika proses login berhasil.
    next_page = reverse_lazy('home')

    # Menambahkan data tambahan ke konteks template.
    def get_context_data(self, **kwargs):
        # Memanggil method asli dari parent class (LoginView).
        context = super().get_context_data(**kwargs)
        # Menambahkan judul halaman ke dalam konteks.
        context['title'] = 'Login Admin'
        # Mengembalikan konteks yang sudah dimodifikasi.
        return context


class LogoutAdminView(LogoutView):
    """
    View untuk menangani proses logout pengguna.
    Cukup mewarisi dari LogoutView bawaan Django dan menentukan halaman tujuan setelah logout.
    """
    # Menentukan URL tujuan (redirect) setelah pengguna berhasil logout.
    next_page = reverse_lazy('login_admin')