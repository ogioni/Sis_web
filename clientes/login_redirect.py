# clientes/login_redirect.py

# Esta função é chamada PELO DJANGO após um login bem-sucedido.
def custom_login_redirect(request):
    user = request.user
    
    # Se o usuário não é um staff (admin), ele vai para a área dele
    if not user.is_staff and user.is_active:
        return '/clientes/area/'
    
    # Caso contrário (se for admin ou staff), vai para o painel de admin.
    return '/admin/'