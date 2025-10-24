from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    # Rota para o formulario publico
    path('cadastro/', views.cadastro_publico_pf, name='cadastro_publico_pf'),
    # Rota para a pagina de sucesso
    path('cadastro/sucesso/', views.cadastro_sucesso, name='cadastro_sucesso'),
]