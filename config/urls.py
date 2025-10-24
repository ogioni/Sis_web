from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

# Personalização do Título do Admin
admin.site.site_header = "Lider Drive - Sistema de Gestão"
admin.site.site_title = "Lider Drive Gestão"
admin.site.index_title = "Bem-vindo ao Sistema Lider Drive"

urlpatterns = [
    # Rota para a RAIZ do site (redireciona para /admin/)
    path('', RedirectView.as_view(url='/admin/', permanent=False)), 
    
    # Rota padrão do Admin
    path('admin/', admin.site.urls),
    
    # Nossas rotas de autenticação CUSTOMIZADAS (login, mudar_senha)
    # E as rotas PADRÃO de recuperação de senha que apontam para os templates em /registration/
    path('contas/', include('users.urls')), 

    # --- LINHA NOVA E IMPORTANTE ---
    # Inclui TODAS as URLs padrão de autenticação do Django (login, logout, password_reset, etc.)
    # Elas também usarão os templates em /registration/ por padrão
    path('contas/', include('django.contrib.auth.urls')), 
    
    # Rota para clientes 
    path('clientes/', include('clientes.urls')), 
]