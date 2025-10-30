# core/models.py

from django.db import models

class SiteConfiguracao(models.Model):
    nome_empresa = models.CharField(
        max_length=100, 
        default='Nome da Empresa',
        help_text="Nome que aparecerá no título da página e cabeçalhos."
    )
    logo = models.ImageField(
        upload_to='logos/', 
        blank=True, 
        null=True, 
        help_text="Faça upload do logo aqui (preferência por PNG transparente)"
    )

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configuração do Site"

    def __str__(self):
        return self.nome_empresa