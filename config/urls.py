from django.contrib import admin
from django.urls import path, include
# IMPORTANTE: Precisamos do TemplateView para mostrar o index.html
from django.views.generic.base import TemplateView 

# Personalização do Título do Admin (continua igual)
admin.site.site_header = "Lider Drive - Sistema de Gestão"
admin.site.site_title = "Lider Drive Gestão"
admin.site.index_title = "Bem-vindo ao Sistema Lider Drive"

urlpatterns = [
    # --- ROTA RAIZ CORRIGIDA ---
    # Agora aponta para o nosso template index.html
    path('', TemplateView.as_view(template_name='index.html'), name='home'), 
    
    # Rota padrão do Admin
    path('admin/', admin.site.urls),
    
    # Nossas rotas de autenticação (login, logout, etc. que usam /accounts/)
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # Nossas rotas customizadas (troca forçada)
    # (Removido o /contas/login/ daqui para evitar duplicação com accounts/)
    path('contas/', include('users.urls')), 
        
    # Rota para clientes (Ainda comentada)
    path('clientes/', include('clientes.urls')), 
]