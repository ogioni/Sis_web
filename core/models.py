# core/models.py

from django.db import models
from django.core.validators import EmailValidator

class SiteConfiguracao(models.Model):
    # 1. Configurações de Marca
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

    # 2. Configurações Dinâmicas de E-mail (Multi-Tenant)
    default_from_email = models.EmailField(
        max_length=254,
        default='naoresponda@exemplo.com',
        validators=[EmailValidator],
        help_text="O e-mail remetente padrão (FROM) que aparecerá para os clientes."
    )
    
    # Detalhes do Serviço SMTP (SendGrid, Mailgun, etc.)
    email_host = models.CharField(
        max_length=100,
        blank=True,
        help_text="Host do servidor SMTP (Ex: smtp.sendgrid.net)"
    )
    email_port = models.IntegerField(
        default=587,
        help_text="Porta do servidor SMTP (Ex: 587 para TLS/STARTTLS)"
    )
    email_host_user = models.CharField(
        max_length=100,
        blank=True,
        help_text="Usuário/API Key do servidor SMTP (Ex: apikey)"
    )
    email_host_password = models.CharField(
        max_length=255,
        blank=True,
        help_text="Senha/API Secret do servidor SMTP (NUNCA armazene em código!)"
    )
    email_use_tls = models.BooleanField(
        default=True,
        help_text="Usar Transport Layer Security (TLS/STARTTLS)?"
    )

    class Meta:
        verbose_name = "Configuração do Site"
        verbose_name_plural = "Configuração do Site"

    def __str__(self):
        return self.nome_empresa

    # MÉTODOS DE AJUDA
    def is_email_config_complete(self):
        """Verifica se as configurações mínimas de e-mail estão presentes."""
        return all([
            self.email_host,
            self.email_host_user,
            self.email_host_password
        ])