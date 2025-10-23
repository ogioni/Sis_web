from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import Group

class ForcePasswordChangeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Qualquer configuração única (na inicialização) vai aqui.

    def __call__(self, request):
        # --- O CÓDIGO RODA AQUI EM TODA REQUISIÇÃO ---

        # 1. Verifica se o usuário está logado
        if request.user.is_authenticated:

            # 2. Tenta encontrar o nosso grupo "marcador"
            try:
                grupo_forcar_mudanca = Group.objects.get(name='Deve Mudar Senha')
            except Group.DoesNotExist:
                # Se o grupo não existir, o middleware não faz nada.
                return self.get_response(request)

            # 3. Verifica se o usuário logado PERTENCE a esse grupo
            if grupo_forcar_mudanca in request.user.groups.all():

                # 4. Pega o caminho da página que o usuário está tentando acessar
                caminho_atual = request.path

                # 5. Define quais páginas são "permitidas" (para evitar um loop infinito)
                url_mudar_senha = reverse('users:mudar_senha')
                url_logout = reverse('admin:logout') # O link de "Sair" do admin

                # Se o usuário está no grupo E NÃO ESTÁ tentando acessar
                # a página de mudar senha ou de sair, nós o FORÇAMOS.
                if caminho_atual not in [url_mudar_senha, url_logout]:

                    # Não podemos deixar ele acessar o /admin, /clientes, etc.
                    # Redireciona ele para a nossa página!
                    return redirect('users:mudar_senha')

        # Se o usuário não está logado, ou não está no grupo,
        # apenas continue normalmente.
        response = self.get_response(request)
        return response