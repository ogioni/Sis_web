from django.contrib.auth.views import PasswordChangeView, LoginView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
# O MiddlewareMixin não é mais necessário aqui se estiver no middleware.py
# from django.utils.deprecation import MiddlewareMixin 
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site

# Views de Autenticação

class MinhaLoginView(LoginView):
    # Aponta para o template GERAL de login (não o do admin)
    template_name = 'paginas/login.html' 
    redirect_authenticated_user = True
    next_page = reverse_lazy('admin:index') # Após login, vai para o admin

class MinhaPasswordChangeView(PasswordChangeView):
    # APONTA PARA O NOVO NOME DO ARQUIVO
    template_name = 'paginas/change_password.html' 
    success_url = reverse_lazy('admin:index') # Após trocar, vai para o admin

    def form_valid(self, form):
        try:
            usuario = self.request.user
            grupo = Group.objects.get(name='Deve Mudar Senha')
            usuario.groups.remove(grupo)
        except Group.DoesNotExist:
            pass
        return super().form_valid(form)

# View customizada de PasswordReset (se necessária para contexto)
class MinhaPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_name'] = get_current_site(self.request).name
        return context