# core/context_processors.py

from .models import SiteConfiguracao

def site_config_processor(request):
    """
    Injeta a configuração do site em todos os templates.
    """
    config = None
    try:
        # Pega a primeira (e única) configuração do site
        config = SiteConfiguracao.objects.first()
    except Exception:
        # O banco de dados pode não estar pronto (ex: durante migrações)
        pass
        
    return {
        'site_config': config,
    }