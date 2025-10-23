from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import MinhaPasswordChangeView # 1. Importa nossa View

# Damos um nome 'app_name' para este arquivo de URLs.
# Isso ajuda o Django a se organizar.
app_name = 'users' 

urlpatterns = [
    # 2. Criamos o endereço:
    # Quando alguém acessar 'mudar-senha/', rode a nossa View.
    # Usamos 'login_required' para proteger a página.
    path(
        'mudar-senha/', 
        login_required(MinhaPasswordChangeView.as_view()), 
        name='mudar_senha'
    ),
]