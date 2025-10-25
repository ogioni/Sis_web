# clientes/login_redirect.py

# A função de redirecionamento (ela é chamada APÓS o login)
def custom_login_redirect(user):
    # Se o usuário é um staff (Admin), ele vai para o painel de controle
    if user.is_staff:
        return '/admin/'
    
    # Se for um usuário comum (Cliente) e estiver ativo, ele vai para a área dele
    # A área do cliente é a rota 'clientes:area_cliente' que mapeia para '/clientes/area/'
    else:
        return '/clientes/area/'