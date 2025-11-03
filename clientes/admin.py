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
    fieldsets = [
        # --- BLOCO 1: DADOS PESSOAIS ---
        ('1. DADOS PESSOAIS', { 
            'classes': ('collapse',), 
            'fields': (
                ('nome_completo', 'data_nascimento'),
                ('cpf', 'rg'),
                ('rg_orgao_expeditor', 'rg_uf', 'estado_civil'),
                ('cnh', 'validade_cnh'), 
            )
        }),
        # --- BLOCO 2: FILIAÇÃO ---
        ('2. FILIAÇÃO', { 
            'classes': ('collapse',), 
            'fields': (
                ('nome_mae', 'nome_pai'),
            )
        }),
        # --- BLOCO 3: CONTATO ---
        ('3. CONTATO', {
            'classes': ('collapse',), 
            'fields': (
                ('email', 'celular', 'telefone'),
            )
        }),
        # --- BLOCO 4: ENDEREÇO RESIDENCIAL ---
        ('4. ENDEREÇO RESIDENCIAL', {
            'classes': ('collapse',), 
            'fields': (
                'cep_residencial',
                ('endereco_residencial', 'numero_residencial', 'complemento_residencial'),
                ('bairro_residencial', 'cidade_residencial', 'estado_residencial'),
            )
        }),
        # --- BLOCO 5: DADOS PROFISSIONAIS ---
        ('5. DADOS PROFISSIONAIS', {
            'classes': ('collapse',), 
            'fields': (
                ('empresa', 'cargo'),
                ('renda_mensal', 'telefone_comercial'),
                'cep_comercial',
                ('endereco_comercial', 'complemento_comercial', 'numero_comercial'),
                ('bairro_comercial', 'cidade_comercial', 'estado_comercial'),
            )
        }),
        # --- BLOCO 6: REFERÊNCIAS ---
        ('6. REFERÊNCIAS', {
            'classes': ('collapse',), 
            'fields': (
                ('ref_pessoal_nome', 'ref_pessoal_telefone'),
                ('ref_bancaria_banco', 'ref_bancaria_agencia', 'ref_bancaria_conta'),
            )
        }),
        # --- BLOCO 7: CONDUTORES ADICIONAIS (CORREÇÃO DE DUPLICAÇÃO E SEPARADORES) ---
        ('7. CONDUTOR 1', { # Separando Condutor 1 em seu próprio Fieldset
            'classes': ('collapse',), 
            'fields': (
                'condutor_nome',
                ('condutor_data_nasc', 'condutor_cpf', 'condutor_cnh', 'condutor_validade_cnh'),
                ('condutor_email', 'condutor_telefone'),
                ('condutor_rg', 'condutor_nome_mae'),
            )
        }),
        ('7. CONDUTOR 2', { # Novo Fieldset para Condutor 2
            'classes': ('collapse',), 
            'fields': (
                'condutor2_nome',
                ('condutor2_data_nasc', 'condutor2_cpf', 'condutor2_cnh', 'condutor2_validade_cnh'),
                ('condutor2_email', 'condutor2_telefone'),
            )
        }),
        ('7. CONDUTOR 3', { # Novo Fieldset para Condutor 3
            'classes': ('collapse',), 
            'fields': (
                'condutor3_nome',
                ('condutor3_data_nasc', 'condutor3_cpf', 'condutor3_cnh', 'condutor3_validade_cnh'),
                ('condutor3_email', 'condutor3_telefone'),
            )
        }),
        # --- BLOCO 8: CONTROLES INTERNOS (Sem modificação, o erro estava no fieldset anterior) ---
        ('8. CONTROLES INTERNOS', {
            'classes': ('collapse',),
            'fields': ('user', 'data_cadastro', 'ativo', 'tipo_pessoa'), 
        })
    ]