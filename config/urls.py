#config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from users.views import MinhaLoginView 

# Personalização do Título do Admin
admin.site.site_header = "Lider Drive - Sistema de Gestão"
admin.site.site_title = "Lider Drive Gestão"
admin.site.index_title = "Bem-vindo ao Sistema Lider Drive"

urlpatterns = [
    # 1. Página Institucional (a que está dando erro)
    path('', TemplateView.as_view(template_name='index.html'), name='home'), 
    
    # 2. Rota de Login Customizada
    path('login/', MinhaLoginView.as_view(template_name='paginas/login.html'), name='login'),
    
    # 3. Rota padrão do Admin
    path('admin/', admin.site.urls),
    
    # 4. URLs de autenticação (troca de senha, etc.)
    path('contas/', include('users.urls')), 
    #path('accounts/', include('django.contrib.auth.urls')), 
    
    # 5. --- CORREÇÃO AQUI ---
    # Inclui TODAS as URLs do app 'clientes' e registra o namespace 'clientes'
    path('clientes/', include('clientes.urls')),
]