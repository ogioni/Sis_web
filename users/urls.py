from django.urls import path
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy # Import reverse_lazy para admin:login
# Importa APENAS as nossas views customizadas
from .views import MinhaPasswordChangeView, MinhaLoginView

# Não usamos app_name aqui

urlpatterns = [
    # 1. Nossas URLs Customizadas
    # Mantemos nosso login geral em /contas/login/, mas o logout vai para /admin/login/
    path('login/', MinhaLoginView.as_view(template_name='paginas/login.html'), name='login'),

    # --- MUDANÇA AQUI ---
    # Agora o logout redireciona para a tela de login DO ADMIN
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('admin:login')), name='logout'),
    # --- FIM DA MUDANÇA ---

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

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        # Após resetar, manda para o login do Admin também
        success_url=reverse_lazy('admin:login')
    ), name='password_reset_confirm'),
]