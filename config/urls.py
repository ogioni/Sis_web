from django.contrib import admin
from django.urls import path, include
# IMPORTANTE: A View da página inicial (index.html) vem daqui
from django.views.generic.base import TemplateView 
# IMPORTANTE: A View de Login customizada vem de 'users'
from users.views import MinhaLoginView 
from clientes.views import ClienteManutencaoView, cadastro_publico_pf, cadastro_sucesso

# Personalização do Título do Admin
admin.site.site_header = "Lider Drive - Sistema de Gestão"
admin.site.site_title = "Lider Drive Gestão"
admin.site.index_title = "Bem-vindo ao Sistema Lider Drive"

urlpatterns = [
    # --- ROTA RAIZ CORRIGIDA ---
    # 1. Página Institucional (Carrega o index.html)
    path('', TemplateView.as_view(template_name='index.html'), name='home'), 
    
    # 2. Rota de Login Customizada (Nosso ponto de entrada não-admin)
    path('login/', MinhaLoginView.as_view(template_name='paginas/login.html'), name='login'),
    
    # 3. Rota padrão do Admin
    path('admin/', admin.site.urls),
    
    # 4. URLs customizadas e padrão auth
    path('contas/', include('users.urls')), 
    path('accounts/', include('django.contrib.auth.urls')), 
    
    # 5. URLs de Clientes (Descomentadas por último)
    path('clientes/cadastro/', cadastro_publico_pf, name='cadastro_publico_pf'),
    path('clientes/cadastro/sucesso/', cadastro_sucesso, name='cadastro_sucesso'),
    # path('clientes/', include('clientes.urls')), # Incluído em detalhe acima para evitar erros
    
]