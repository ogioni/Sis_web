from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
# IMPORTAÇÃO CORRETA
from .views import MinhaPasswordChangeView, MinhaLoginView, MinhaPasswordResetView 

app_name = 'users'

urlpatterns = [
    # 1. Login/Logout Personalizado
    path('login/', MinhaLoginView.as_view(), name='login'), 
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # 2. Mudar Senha Personalizado (Troca Forçada)
    path(
        'mudar-senha/', 
        login_required(MinhaPasswordChangeView.as_view()), 
        name='mudar_senha'
    ),
    
    # 3. ROTAS DE RECUPERAÇÃO DE SENHA (USANDO A NOVA VIEW)
   path('recuperar-senha/', auth_views.PasswordResetView.as_view(
        email_template_name='paginas/recuperar_senha_email.html',
        subject_template_name='paginas/recuperar_senha_subject.txt',
        success_url=reverse_lazy('users:recuperar_senha_done')
    ), name='recuperar_senha'),

    path('recuperar-senha/done/', auth_views.PasswordResetDoneView.as_view(), 
         name='recuperar_senha_done'),
    
    path('recuperar-senha/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='paginas/recuperar_senha_confirm.html',
        # Redireciona diretamente para o login após mudar a senha
        success_url=reverse_lazy('users:login') 
    ), name='recuperar_senha_confirm'),
]