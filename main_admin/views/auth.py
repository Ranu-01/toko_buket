from django.views.generic import CreateView
from ..forms import RegistrasiAdminForm, LoginAdminForm
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView






class RegistrasiView(CreateView):
   
    form_class = RegistrasiAdminForm
    template_name = 'admin/auth/register.html'
    # Setelah registrasi berhasil, arahkan ke halaman login
    success_url = reverse_lazy('login_admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registrasi Admin Baru'
        return context

class LoginAdminView(LoginView):
 
    form_class = LoginAdminForm
    template_name = 'admin/auth/login.html'
    # Halaman yang akan dituju setelah login berhasil
    next_page = reverse_lazy('home') # Ganti 'home' dengan nama URL dashboard admin Anda

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login Admin'
        return context

class LogoutAdminView(LogoutView):
    """
    View untuk menangani proses logout.
    """
    # Halaman yang akan dituju setelah logout berhasil
    next_page = reverse_lazy('login_admin')
