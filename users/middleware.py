from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import Group
from django.conf import settings 

class MinhaPasswordChangeMiddleware(MiddlewareMixin):
    
    def process_request(self, request):
        
        if not request.user.is_authenticated or request.user.is_superuser:
            return None
        
        try:
            # --- MUDANÇA AQUI ---
            url_change_password = reverse('change_password') # NOVO NOME DA URL
            url_logout = reverse('logout') # Nome global agora
        except Exception:
            # Se as URLs ainda não carregaram (raro), ignora
            return None 

        excluded_urls = [
            settings.LOGIN_URL,  
            url_change_password, # Usa a variável com novo nome
            url_logout,          
            '/'                  
        ]
        
        if request.path in excluded_urls:
            return None
        
        try:
            if request.user.groups.filter(name='Deve Mudar Senha').exists():
                # --- MUDANÇA AQUI ---
                return redirect(url_change_password) # Redireciona para a URL com novo nome
        except Group.DoesNotExist:
            return None 
        except Exception:
            return None

        return None