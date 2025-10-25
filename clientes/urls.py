from django.urls import path
from .views import cadastro_publico_pf, cadastro_sucesso, area_cliente_logado

app_name = 'clientes'

urlpatterns = [
    # Rota para o formulario publico
    path('cadastro/', cadastro_publico_pf, name='cadastro_publico_pf'),
    
    # Rota para a pagina de sucesso
    path('cadastro/sucesso/', cadastro_sucesso, name='cadastro_sucesso'),
    
   # --- ROTA PARA A ÁREA EXCLUSIVA (após login) ---
    path('area/', area_cliente_logado, name='area_cliente'),
]