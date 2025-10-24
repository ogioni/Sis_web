from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'celular', 'email', 'ativo')
    search_fields = ('nome_completo', 'cpf', 'email')
    list_filter = ('ativo', 'tipo_pessoa', 'cidade_residencial')
    ordering = ('nome_completo',)

    # --- MUDANÇAS AQUI (Títulos dos Fieldsets) ---
    fieldsets = (
        ('Internal Controls', { # Traduzido
            'fields': ('ativo', 'tipo_pessoa')
        }),
        ('Personal Info', { # Traduzido
            'fields': (
                'nome_completo', 'data_nascimento', 'rg', 'cpf', 'cnh', 
                'validade_cnh', 'nome_mae', 'nome_pai', 'estado_civil',
                'email', 'telefone', 'celular'
            )
        }),
        ('Home Address', { # Traduzido
            'classes': ('collapse',), 
            'fields': (
                'cep_residencial', 'endereco_residencial', 'numero_residencial',
                'bairro_residencial', 'cidade_residencial', 'estado_residencial'
            )
        }),
        ('Professional Info', { # Traduzido
            'classes': ('collapse',),
            'fields': (
                'empresa', 'cargo', 'renda_mensal', 'telefone_comercial',
                'cep_comercial', 'endereco_comercial'
            )
        }),
        ('References', { # Traduzido
            'classes': ('collapse',),
            'fields': (
                'ref_pessoal_nome', 'ref_pessoal_telefone',
                'ref_bancaria_banco', 'ref_bancaria_agencia', 'ref_bancaria_conta'
            )
        }),
        ('Additional Driver', { # Traduzido
            'classes': ('collapse',),
            'fields': (
                'condutor_nome', 'condutor_data_nasc', 'condutor_rg', 
                'condutor_cpf', 'condutor_cnh', 'condutor_validade_cnh',
                'condutor_nome_mae', 'condutor_email', 'condutor_telefone'
            )
        }),
    )