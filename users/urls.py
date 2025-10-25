from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy 

# Importa NOSSAS views customizadas
from .views import (
    MinhaPasswordChangeView, 
    MinhaLoginView, 
    MinhaPasswordResetConfirmView # <-- IMPORTANDO O NOME CORRETO
)

# ATENÇÃO: Removemos o app_name = 'users' para usar os nomes padrão do Django
# app_name = 'users' 

urlpatterns = [
    # 1. Nossas URLs Customizadas
    # (Usamos a do admin:login, então esta é secundária)
    path('login/', MinhaLoginView.as_view(template_name='paginas/login.html'), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('admin:login')), name='logout'), 
    
    path(
        'change_password/', 
        login_required(MinhaPasswordChangeView.as_view()), 
        name='change_password' 
    ),
    
    # --- ROTAS PADRÃO DE RECUPERAÇÃO DE SENHA ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html', 
        subject_template_name='registration/password_reset_subject.txt',
        success_url=reverse_lazy('password_reset_done') 
    ), name='password_reset'), 

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'), 
    
    # --- CORREÇÃO AQUI ---
    # Agora usa o nome da classe correto: MinhaPasswordResetConfirmView
    path('reset/<uidb64>/<token>/', MinhaPasswordResetConfirmView.as_view(), 
        name='password_reset_confirm'), 
    # --- FIM DA CORREÇÃO ---
]