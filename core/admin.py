# core/admin.py

from django.contrib import admin
from .models import SiteConfiguracao

@admin.register(SiteConfiguracao)
class SiteConfiguracaoAdmin(admin.ModelAdmin):
    list_display = ('nome_empresa',)

    # Lógica do "Singleton" (Modelo de Instância Única)
    # Impede que o usuário crie uma *nova* configuração se uma já existir.
    def has_add_permission(self, request):
        return not SiteConfiguracao.objects.exists()

    # Impede que o usuário delete a configuração
    def has_delete_permission(self, request, obj=None):
        return False