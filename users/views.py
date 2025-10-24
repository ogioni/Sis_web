from django.contrib.auth.views import PasswordChangeView, LoginView, PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site

# Views de Autenticação

class MinhaLoginView(LoginView):
    template_name = 'paginas/login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('admin:index') 

class MinhaPasswordChangeView(PasswordChangeView):
    template_name = 'paginas/mudar_senha.html'
    success_url = reverse_lazy('admin:index') 

    def form_valid(self, form):
        # Lógica para remover o usuário do grupo "Deve Mudar Senha"
        try:
            usuario = self.request.user
            grupo = Group.objects.get(name='Deve Mudar Senha')
            usuario.groups.remove(grupo)
        except Group.DoesNotExist:
            pass
        
        return super().form_valid(form)

# VIEW DE RECUPERAÇÃO PERSONALIZADA (CORREÇÃO DE CONTEXTO)
class MinhaPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm 
    
    # Opcional, mas ajuda a garantir o contexto do e-mail
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Garante que o template do e-mail tenha acesso correto ao Site
        context['site_name'] = get_current_site(self.request).name
        return context