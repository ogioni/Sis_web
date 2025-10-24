from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import Group
from django.conf import settings # Importa o settings para pegar a LOGIN_URL

class MinhaPasswordChangeMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        
        # 1. Ignora quem não está logado ou é Superusuário
        if not request.user.is_authenticated or request.user.is_superuser:
            return None
        
        # 2. Define as URLs que devem ser excluídas do bloqueio (para evitar loop)
        try:
            url_mudar_senha = reverse('users:mudar_senha')
            url_logout = reverse('users:logout') 
        except Exception:
            # Caso o Django ainda não tenha carregado as rotas, retorna None
            return None 

        excluded_urls = [
            settings.LOGIN_URL,  # A URL que o Django vai tentar te mandar
            url_mudar_senha,     # A página que queremos que ele acesse
            url_logout,          # A opção de sair
            '/'                  # Permite o acesso à página inicial (opcional, mas seguro)
        ]
        
        # Se o usuário está tentando acessar uma página permitida, deixe-o.
        if request.path in excluded_urls:
            return None
        
        # 3. Lógica Principal: Se o usuário é do grupo "Deve Mudar Senha"
        try:
            if request.user.groups.filter(name='Deve Mudar Senha').exists():
                # Redireciona à força para a página de mudar senha
                return redirect(url_mudar_senha)
        except Group.DoesNotExist:
            return None # O grupo não existe no banco, ignora
        except Exception:
            return None

        return None