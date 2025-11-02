# clientes/admin.py

from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    # 1. Configuração da listagem
    list_display = ('nome_completo', 'cpf', 'celular', 'email', 'data_cadastro', 'ativo')
    list_filter = ('ativo', 'tipo_pessoa', 'estado_residencial')
    search_fields = ('nome_completo', 'cpf', 'email', 'celular')
    ordering = ('nome_completo',)
    
    # Campos que não devem ser alterados manualmente no Admin
    readonly_fields = ('data_cadastro', 'user') 

    # 2. DEFINIÇÃO DA ORDEM E AGRUPAMENTO DOS CAMPOS (Fieldsets)
    # Todos os fieldsets terão 'classes': ('collapse',), para iniciar fechados.
    fieldsets = [
        # --- BLOCO 1: DADOS PESSOAIS (AGORA COM CNH) ---
        ('1. DADOS PESSOAIS', { # Título ajustado para refletir CNH
            'classes': ('collapse',), 
            'fields': (
                ('nome_completo', 'data_nascimento'),
                ('cpf', 'rg'),
                ('rg_orgao_expeditor', 'rg_uf', 'estado_civil'),
                # CNH MOVIDA PARA CÁ
                ('cnh', 'validade_cnh'), 
            )
        }),
        # --- BLOCO 2: FILIAÇÃO (REMOVEMOS CNH) ---
        ('2. FILIAÇÃO', { # Título ajustado para apenas Filiação
            'classes': ('collapse',), 
            'fields': (
                ('nome_mae', 'nome_pai'),
                # CNH foi removida daqui
            )
        }),
        # --- BLOCOS SEGUINTES PERMANECEM INALTERADOS ---
        ('3. CONTATO', {
            'classes': ('collapse',), 
            'fields': (
                ('email', 'celular', 'telefone'),
            )
        }),
        ('4. ENDEREÇO RESIDENCIAL', {
            'classes': ('collapse',), 
            'fields': (
                'cep_residencial',
                ('endereco_residencial', 'numero_residencial', 'complemento_residencial'),
                ('bairro_residencial', 'cidade_residencial', 'estado_residencial'),
            )
        }),
        ('5. DADOS PROFISSIONAIS', {
            'classes': ('collapse',), 
            'fields': (
                ('empresa', 'cargo'),
                ('renda_mensal', 'telefone_comercial'),
                'cep_comercial',
                ('endereco_comercial', 'complemento_comercial'),
            )
        }),
        ('6. REFERÊNCIAS', {
            'classes': ('collapse',), 
            'fields': (
                ('ref_pessoal_nome', 'ref_pessoal_telefone'),
                ('ref_bancaria_banco', 'ref_bancaria_agencia', 'ref_bancaria_conta'),
            )
        }),
        ('7. CONDUTOR ADICIONAL', {
            'classes': ('collapse',), 
            'fields': (
                'condutor_nome',
                ('condutor_data_nasc', 'condutor_rg', 'condutor_cpf'),
                ('condutor_cnh', 'condutor_validade_cnh'),
                'condutor_nome_mae',
                ('condutor_email', 'condutor_telefone'),
            )
        }),
        ('8. CONTROLES INTERNOS', {
            'classes': ('collapse',),
            'fields': ('user', 'data_cadastro', 'ativo', 'tipo_pessoa'), 
        })
    ]