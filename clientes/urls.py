#clientes/urls.py

from django.urls import path
# Importe a LoginView padrão do Django
from django.contrib.auth.views import LoginView

from .views import (
    cadastro_publico_pf, 
    cadastro_sucesso, 
    area_cliente_logado,
    cadastro_dinamico_view,
    verificar_documento_ajax # ADICIONADO
)

app_name = 'clientes'

urlpatterns = [
    # Rota para o formulario publico (Legado)
    path('cadastro/', cadastro_publico_pf, name='cadastro_publico_pf'),
    
    # --- NOVO FLUXO DINÂMICO ---
    path('novo/', cadastro_dinamico_view, name='cadastro_dinamico'), 
    
    # Rota AJAX para verificação de documento
    path('verificar-doc/', verificar_documento_ajax, name='verificar_documento_ajax'), # ADICIONADO
    
    # Rota para a pagina de sucesso
    path('cadastro/sucesso/', cadastro_sucesso, name='cadastro_sucesso'),
    
    # --- ROTA PARA A ÁREA EXCLUSIVA (após login) ---
    path('area/', area_cliente_logado, name='area_cliente'),

    # --- ROTA PARA A NOVA TELA DE LOGIN DO CLIENTE ---
    path(
        'login/', 
        LoginView.as_view(
            template_name='clientes/login_cliente.html',
            redirect_authenticated_user=True # Se já tiver logado, vai pro redirect
        ), 
        name='login_cliente'
    ),
]