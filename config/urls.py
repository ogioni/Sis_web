# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView 
from users.views import MinhaLoginView
from django.views.i18n import JavaScriptCatalog # <-- 1. IMPORTAR AQUI

# Personalização do Título do Admin
admin.site.site_header = "Lider Drive - Sistema de Gestão"
admin.site.site_title = "Lider Drive Gestão"
admin.site.index_title = "Bem-vindo ao Sistema Lider Drive"

urlpatterns = [
    # 1. Página Institucional
    path('', TemplateView.as_view(template_name='index.html'), name='home'), 
    
    # 2. Rota de Login Customizada (A nossa "Porta da Frente")
    path('login/', MinhaLoginView.as_view(template_name='paginas/login.html'), name='login'),
    
    # 3. Rota padrão do Admin (A "Porta dos Fundos")
    path('admin/', admin.site.urls),
    
    # 4. URLs de autenticação (troca de senha, etc.)
    path('contas/', include('users.urls')), 
    #path('accounts/', include('django.contrib.auth.urls')), 
    
    # 5. URLs do app 'clientes'
    path('clientes/', include('clientes.urls')),

    # 6. --- (NOVO) URL JSI18N PARA O SCRIPT DO TEMA ---
    # Esta linha é necessária para o script admin/js/theme.js funcionar
    path('jsi18n/', JavaScriptCatalog.as_view(), name='jsi18n'),
]