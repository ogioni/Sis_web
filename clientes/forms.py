# clientes/forms.py

from django import forms
from .models import Cliente
from django.contrib.auth.models import User
import re # Para limpar o CPF

# --- FUNÇÃO DE VALIDAÇÃO DE CPF (Algoritmo) ---
# ESTA FUNÇÃO FOI RESTAURADA AQUI
def validate_cpf_algorithm(cpf_limpo):
    if len(cpf_limpo) != 11 or cpf_limpo == cpf_limpo[0] * 11:
        return False
    # Algoritmo de validação (Dígito 1)
    sum_ = 0
    for i in range(9):
        sum_ += int(cpf_limpo[i]) * (10 - i)
    rev = (sum_ * 10) % 11
    if rev == 10: rev = 0
    if rev != int(cpf_limpo[9]):
        return False
    # (Dígito 2)
    sum_ = 0
    for i in range(10):
        sum_ += int(cpf_limpo[i]) * (11 - i)
    rev = (sum_ * 10) % 11
    if rev == 10: rev = 0
    if rev != int(cpf_limpo[10]):
        return False
    return True
# --- FIM DA FUNÇÃO ---

# --- OPÇÕES PARA OS DROPDOWNS (SELECTS) ---
UF_CHOICES = [
    ('', 'Selecione...'), ('AC', 'AC'), ('AL', 'AL'), ('AP', 'AP'), ('AM', 'AM'),
    ('BA', 'BA'), ('CE', 'CE'), ('DF', 'DF'), ('ES', 'ES'),
    ('GO', 'GO'), ('MA', 'MA'), ('MT', 'MT'), ('MS', 'MS'),
    ('MG', 'MG'), ('PA', 'PA'), ('PB', 'PB'), ('PR', 'PR'),
    ('PE', 'PE'), ('PI', 'PI'), ('RJ', 'RJ'), ('RN', 'RN'),
    ('RS', 'RS'), ('RO', 'RO'), ('RR', 'RR'), ('SC', 'SC'),
    ('SP', 'SP'), ('SE', 'SE'), ('TO', 'TO'),
]

ESTADO_CIVIL_CHOICES = [
    ('', 'Selecione...'), ('SOLTEIRO(A)', 'SOLTEIRO(A)'),
    ('CASADO(A)', 'CASADO(A)'), ('SEPARADO(A)', 'SEPARADO(A)'),
    ('DIVORCIADO(A)', 'DIVORCIADO(A)'), ('VIUVO(A)', 'VIÚVO(A)'), 
]
# --- FIM DAS OPÇÕES ---


# --- FORMULÁRIO PARA A FASE 1 (Auto-Registro - CORRIGIDO) ---
class FichaCadastralClienteForm(forms.ModelForm):
    
    # Adicionando (*) aos campos obrigatórios (required=True)
    nome_completo = forms.CharField(label='Nome Completo (*)', widget=forms.TextInput(attrs={'required': True, 'class': 'uppercase-input'}))
    data_nascimento = forms.DateField(label='Data de Nascimento (*)', widget=forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'required': True}))
    cpf = forms.CharField(label='CPF (*)', widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'required': True}))
    rg = forms.CharField(label='RG (*)', required=True, widget=forms.TextInput(attrs={'required': True, 'class': 'uppercase-input'}))
    rg_uf = forms.ChoiceField(label='UF RG (*)', choices=UF_CHOICES, widget=forms.Select(attrs={'required': True}))
    rg_orgao_expeditor = forms.CharField(label='Órgão Expedidor (*)', widget=forms.TextInput(attrs={'required': True, 'class': 'uppercase-input'}))
    estado_civil = forms.ChoiceField(label='Estado Civil (*)', choices=ESTADO_CIVIL_CHOICES, widget=forms.Select(attrs={'required': True}))
    nome_mae = forms.CharField(label='Nome da Mãe (*)', widget=forms.TextInput(attrs={'required': True, 'class': 'uppercase-input'}))
    
    # Estes continuam como antes (não obrigatórios ou especiais)
    nome_pai = forms.CharField(label='Nome do Pai', required=False, widget=forms.TextInput(attrs={'class': 'uppercase-input'}))
    telefone = forms.CharField(label='Telefone (Fixo)', required=False, widget=forms.TextInput(attrs={'placeholder': '(00) 0000-0000'}))

    # Campos de E-mail e Celular (Também obrigatórios)
    email = forms.EmailField(label='E-mail (*)', widget=forms.EmailInput(attrs={'required': True, 'class': 'lowercase-input'}))
    email_confirm = forms.EmailField(label='Confirme seu E-mail (*)', widget=forms.EmailInput(attrs={'required': True, 'class': 'lowercase-input'}))
    celular = forms.CharField(label='Celular (*)', widget=forms.TextInput(attrs={'required': True, 'placeholder': '(00) 0.0000-0000'}))
    
    
    class Meta:
        model = Cliente
        fields = [
            'nome_completo', 'data_nascimento', 'cpf', 'rg', 
            'rg_orgao_expeditor', 'rg_uf', 'estado_civil',
            'nome_mae', 'nome_pai', 'telefone', 'celular', 
            'email', 'email_confirm'
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf_limpo = re.sub(r'[^\d]', '', str(cpf)) 
        if not validate_cpf_algorithm(cpf_limpo): # <-- Agora a função é visível
            raise forms.ValidationError('CPF inválido.')
        if Cliente.objects.filter(cpf=cpf_limpo).exists():
            raise forms.ValidationError('Cliente com esse CPF ja cadastrado!')
        return cpf_limpo 

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email: 
              return email
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso por outro usuário.')
        return email.lower() 
    
    def clean_email_confirm(self):
        email_confirm = self.cleaned_data.get('email_confirm')
        if not email_confirm:
            return email_confirm
        return email_confirm.lower() 

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_confirm = cleaned_data.get('email_confirm')
        if email and email_confirm and email != email_confirm:
            self.add_error('email_confirm', "Os e-mails fornecidos não são iguais.")
        return cleaned_data

# ---
# --- PASSO 454 (O NOVO CÓDIGO) ---
# ---
# --- FORMULÁRIO PARA A FASE 3 (Manutenção da Ficha Completa) ---
# --- Este formulário será usado pelo cliente logado para ATUALIZAR seus dados ---

class ClienteManutencaoForm(forms.ModelForm):
    
    class Meta:
        model = Cliente
        # Pega TODOS os campos do Modelo Cliente
        fields = '__all__'
        
        # Exclui os campos que o cliente NÃO PODE editar
        exclude = ('user', 'data_cadastro', 'ativo', 'tipo_pessoa')
        
        # Opcional: Adicionar classes CSS para máscaras e uppercase
        # (O JS vai pegar os IDs, então isso é mais para o 'uppercase-input')
        widgets = {
            # --- Dados Pessoais ---
            'nome_completo': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'data_nascimento': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA'}),
            'cpf': forms.TextInput(attrs={'readonly': True}), # Não deixa mudar o CPF
            'rg': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'rg_orgao_expeditor': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'rg_uf': forms.Select(), # As opções virão do modelo
            'cnh': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'validade_cnh': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA'}),
            'nome_mae': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'nome_pai': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'estado_civil': forms.Select(), # As opções virão do modelo
            
            # Contato
            'email': forms.EmailInput(attrs={'readonly': True}), # Não deixa mudar o email (username)
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 0000-0000'}),
            'celular': forms.TextInput(attrs={'placeholder': '(00) 0.0000-0000'}),

            # Endereço Residencial
            'cep_residencial': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'endereco_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'numero_residencial': forms.TextInput(),
            'bairro_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'cidade_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'estado_residencial': forms.Select(),

            # Dados Profissionais
            'empresa': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'cargo': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'renda_mensal': forms.NumberInput(attrs={'placeholder': '0.00'}),
            'telefone_comercial': forms.TextInput(attrs={'placeholder': '(00) 0000-0000'}),
            'cep_comercial': forms.TextInput(attrs={'placeholder': '00000-000'}),
            'endereco_comercial': forms.TextInput(attrs={'class': 'uppercase-input'}),

            # Referências
            'ref_pessoal_nome': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'ref_pessoal_telefone': forms.TextInput(attrs={'placeholder': '(00) 0.0000-0000'}),
            'ref_bancaria_banco': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'ref_bancaria_agencia': forms.TextInput(),
            'ref_bancaria_conta': forms.TextInput(),

            # Condutor Adicional
            'condutor_nome': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_data_nasc': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA'}),
            'condutor_rg': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00'}),
            'condutor_cnh': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_validade_cnh': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA'}),
            'condutor_nome_mae': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_email': forms.EmailInput(),
            'condutor_telefone': forms.TextInput(attrs={'placeholder': '(00) 0.0000-0000'}),
        }