# clientes/urls.py

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
    cadastro_publico_pf, 
    cadastro_sucesso, 
    area_cliente_logado,
    cadastro_dinamico_view,
    verificar_documento_ajax,
    ClienteManutencaoView,  # Class-Based View para edição
)

app_name = 'clientes'

urlpatterns = [
    # --- Formulário público legado ---
    path('cadastro/', cadastro_publico_pf, name='cadastro_publico_pf'),
    
    # --- Novo fluxo dinâmico ---
    path('novo/', cadastro_dinamico_view, name='cadastro_dinamico'), 
    path('verificar-doc/', verificar_documento_ajax, name='verificar_documento_ajax'), 
    path('cadastro/sucesso/', cadastro_sucesso, name='cadastro_sucesso'),
    
    # --- Área exclusiva do cliente (após login) ---
    path('area/', area_cliente_logado, name='area_cliente'),
    path('area/editar/', ClienteManutencaoView.as_view(), name='ficha_cadastral'),  # edição da ficha cadastral

    # --- Autenticação ---
    path(
        'login/', 
        LoginView.as_view(
            template_name='clientes/login_cliente.html',
            redirect_authenticated_user=True
        ), 
        name='login_cliente'
    ),
    path(
        'logout/',
        LogoutView.as_view(next_page='clientes:login_cliente'),
        name='logout_cliente'
    ),
]