# core/admin.py

from django.contrib import admin
from .models import SiteConfiguracao

@admin.register(SiteConfiguracao)
class SiteConfiguracaoAdmin(admin.ModelAdmin):
    # Campos que aparecerão na lista de configuração (overview)
    list_display = ('nome_empresa', 'default_from_email', 'email_host')

    # Organização visual da tela de edição (Onde a mágica acontece!)
    fieldsets = (
        ('1. CONFIGURAÇÃO DE MARCA E IDENTIDADE', {
            'fields': ('nome_empresa', 'logo',),
            'description': 'Configure o nome e logo que serão vistos pelo cliente final.'
        }),
        ('2. CONFIGURAÇÃO DE E-MAIL REMETENTE', {
            'fields': ('default_from_email',),
            'description': 'O endereço de e-mail que aparecerá como remetente (De:).'
        }),
        ('3. CREDENCIAIS DO SERVIDOR DE E-MAIL (SMTP)', {
            'fields': ('email_host', 'email_port', 'email_use_tls', 'email_host_user', 'email_host_password'),
            'description': 'Insira as credenciais do seu provedor (SendGrid, AWS SES, etc.). Deixar em branco usará o Console/Settings padrão.'
        }),
    )

    # Lógica do "Singleton" (Modelo de Instância Única)
    # Impede que o usuário crie uma *nova* configuração se uma já existir.
    def has_add_permission(self, request):
        return not SiteConfiguracao.objects.exists()

    # Impede que o usuário delete a configuração
    def has_delete_permission(self, request, obj=None):
        return False