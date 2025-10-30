# users/urls.py

from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy 

# Importa NOSSAS views customizadas
from .views import (
    MinhaPasswordChangeView, 
    MinhaLoginView, 
    MinhaPasswordResetConfirmView,
    resend_activation_view
)

urlpatterns = [
    # 1. URL DE LOGOUT CORRIGIDA: Redireciona para o login PÚBLICO
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'), 
    
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
    
    # --- USA A NOSSA VIEW CUSTOMIZADA DE CONFIRMAÇÃO ---
    path('reset/<uidb64>/<token>/', MinhaPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'), 

    # --- ROTA PARA REENVIAR ATIVAÇÃO ---
    path(
        'reenviar-ativacao/', 
        resend_activation_view, 
        name='reenviar_ativacao'
    ),
]