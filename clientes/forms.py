from django import forms
from .models import Cliente

# --- FORMULÁRIO PARA A FASE 1 (Auto-Registro, Dados Essenciais) ---
class FichaCadastralClienteForm(forms.ModelForm):
    # Campo de confirmação de email (não está no modelo, é só para validação)
    email_confirm = forms.EmailField(label='Confirme seu E-mail') 

    class Meta:
        model = Cliente
        # AQUI É ONDE DEFINIMOS A ORDEM LÓGICA E AS MUDANÇAS DE ORDEM
        fields = [
            'nome_completo', 
            'data_nascimento', 
            'cpf', 
            'estado_civil',       # MUDANÇA: Subiu para L2
            'rg',                 # MUDANÇA: Desceu para L3
            'rg_orgao_expeditor', # MUDANÇA: Novo label será 'Orgão Expedidor'
            'rg_uf',              # MUDANÇA: Novo label será 'UF RG'
            'nome_mae', 
            'nome_pai',
            'telefone', 
            'celular', 
            'email',
            'email_confirm', 
        ]
        
        # MUDANÇA: Customização dos labels
        labels = {
            'estado_civil': 'Estado Civil', # Manter, mas reordenado
            'rg': 'RG',                     # Manter, mas reordenado
            'rg_orgao_expeditor': 'Órgão Expedidor', # Label corrigido
            'rg_uf': 'UF RG',               # Label corrigido
        }
        
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')

        if email and email_confirm and email != email_confirm:
            self.add_error('email_confirm', "Os e-mails fornecidos não são iguais.")
        return cleaned_data