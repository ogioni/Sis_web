# clientes/forms.py

from django import forms
from .models import Cliente
from django.contrib.auth.models import User
import re # Para limpar o CPF

# --- FUNÇÃO DE VALIDAÇÃO DE CPF (Algoritmo) ---
def validate_cpf_algorithm(cpf_limpo):
# ... (código validate_cpf_algorithm inalterado) ...
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
# --- FIM DA FUNÇÃO CPF ---

# --- [NOVO] FUNÇÃO DE VALIDAÇÃO DE CNPJ (Algoritmo) ---
def validate_cnpj_algorithm(cnpj_limpo):
# ... (código validate_cnpj_algorithm inalterado) ...
    if len(cnpj_limpo) != 14 or cnpj_limpo == cnpj_limpo[0] * 14:
        return False

    def calcular_digito(digitos, pesos):
        soma = sum(int(d) * p for d, p in zip(digitos, pesos))
        resto = soma % 11
        return 0 if resto < 2 else 11 - resto

    # Pesos para o primeiro dígito
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    # Pesos para o segundo dígito
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]

    # Calcula primeiro dígito
    digitos_base1 = cnpj_limpo[:12]
    dv1 = calcular_digito(digitos_base1, pesos1)
    if dv1 != int(cnpj_limpo[12]):
        return False

    # Calcula segundo dígito
    digitos_base2 = cnpj_limpo[:13] # Inclui o primeiro dígito calculado
    dv2 = calcular_digito(digitos_base2, pesos2)
    if dv2 != int(cnpj_limpo[13]):
        return False

    return True
# --- FIM DA FUNÇÃO CNPJ ---


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


# --- FORMULÁRIO PARA A FASE 1 (Auto-Registro - COM NOVAS VALIDAÇÕES) ---
class FichaCadastralClienteForm(forms.ModelForm):
# ... (código FichaCadastralClienteForm inalterado) ...
    
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
    celular = forms.CharField(label='Celular (*)', widget=forms.TextInput(attrs={'required': True, 'placeholder': '(00) 9.0000-0000'})) # Ajustado para novo padrão
    
    
    class Meta:
        model = Cliente
        fields = [
            'nome_completo', 'data_nascimento', 'cpf', 'rg', 
            'rg_orgao_expeditor', 'rg_uf', 'estado_civil',
            'nome_mae', 'nome_pai', 'telefone', 'celular', 
            'email', 'email_confirm'
        ]

    # ... (Métodos clean_ inalterados) ...
    def clean_nome_completo(self):
        nome = self.cleaned_data.get('nome_completo')
        if nome:
            if '.' in nome:
                raise forms.ValidationError("Nome não pode conter pontos (.).")
            # Remove espaços extras antes de dividir para evitar contagem errada
            partes = [parte for parte in nome.split(' ') if parte] 
            if len(partes) < 2:
                raise forms.ValidationError("Por favor, informe o nome completo.")
        return nome

    def clean_nome_mae(self):
        nome = self.cleaned_data.get('nome_mae')
        if nome:
            if '.' in nome:
                raise forms.ValidationError("Nome da mãe não pode conter pontos (.).")
            # Remove espaços extras antes de dividir
            partes = [parte for parte in nome.split(' ') if parte]
            if len(partes) < 2:
                raise forms.ValidationError("Por favor, informe o nome completo da mãe.")
        return nome
    # --- FIM DAS NOVAS VALIDAÇÕES ---

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        cpf_limpo = re.sub(r'[^\d]', '', str(cpf)) 
        if not validate_cpf_algorithm(cpf_limpo):
            raise forms.ValidationError('CPF inválido.')
        # Verifica duplicidade APENAS se o CPF for válido
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
# --- FORMULÁRIO PARA A FASE 3 (Manutenção da Ficha Completa) ---
class ClienteManutencaoForm(forms.ModelForm):
    
    # *** CORREÇÃO CRÍTICA #1: Sobrescreve o campo CPF para ignorar a validação de max_length=11 do ModelForm/Model.
    # Usamos CharField sem especificar max_length no form.
    cpf = forms.CharField(label='CPF', required=False, 
                          widget=forms.TextInput(attrs={'readonly': True, 'class': 'cpf-mask'}))

    # *** CORREÇÃO CRÍTICA #2: Sobrescreve o campo condutor_cpf para aceitar 14 dígitos (CNPJ) sem erro.
    condutor_cpf = forms.CharField(label='CPF/CNPJ do Condutor', required=False, 
                                   widget=forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'cpf-mask'}))


    class Meta:
        model = Cliente
        # Aqui definimos a ordem e incluímos os novos campos
        fields = (
            'nome_completo', 'data_nascimento', 'cpf', 'rg', 
            'rg_orgao_expeditor', 'rg_uf', 'estado_civil',
            'nome_mae', 'nome_pai', 'cnh', 'validade_cnh',
            
            'email', 'telefone', 'celular',
            
            # Endereço Residencial (NOVA ORDEM COM COMPLEMENTO)
            'cep_residencial', 'endereco_residencial', 
            'numero_residencial', 'complemento_residencial', 
            'bairro_residencial', 'cidade_residencial', 'estado_residencial',
            
            # Dados Profissionais
            'empresa', 'cargo', 'renda_mensal', 'telefone_comercial', 
            'cep_comercial', 'endereco_comercial', 'complemento_comercial', 
            
            # Referências
            'ref_pessoal_nome', 'ref_pessoal_telefone', 
            'ref_bancaria_banco', 'ref_bancaria_agencia', 'ref_bancaria_conta',
            
            # Condutor Adicional
            'condutor_nome', 'condutor_data_nasc', 'condutor_rg', 'condutor_cpf', 
            'condutor_cnh', 'condutor_validade_cnh', 'condutor_nome_mae', 
            'condutor_email', 'condutor_telefone',
            
            # Controles Internos
            'data_cadastro', 'ativo', 'tipo_pessoa', 'user',
        )
        exclude = ('user', 'data_cadastro', 'ativo', 'tipo_pessoa')
        widgets = {
            # --- Dados Pessoais ---
            'nome_completo': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'data_nascimento': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'class': 'date-mask'}),
            'cpf': forms.TextInput(attrs={'readonly': True, 'class': 'cpf-mask'}), 
            'rg': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'rg_orgao_expeditor': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'rg_uf': forms.Select(choices=UF_CHOICES), 
            'cnh': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'validade_cnh': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'class': 'date-mask'}),
            'nome_mae': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'nome_pai': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'estado_civil': forms.Select(choices=ESTADO_CIVIL_CHOICES), 
            
            # Contato
            'email': forms.EmailInput(attrs={'readonly': True}), 
            'telefone': forms.TextInput(attrs={'placeholder': '(00) 0000-0000', 'class': 'phone-mask-fixo'}),
            'celular': forms.TextInput(attrs={'placeholder': '(00) 9.0000-0000', 'class': 'phone-mask-celular'}),

            # Endereço Residencial
            'cep_residencial': forms.TextInput(attrs={'placeholder': '00000-000', 'class': 'cep-mask'}),
            'endereco_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'numero_residencial': forms.TextInput(),
            'complemento_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}), 
            'bairro_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'cidade_residencial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'estado_residencial': forms.Select(choices=UF_CHOICES),

            # Dados Profissionais
            'empresa': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'cargo': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'renda_mensal': forms.NumberInput(attrs={'placeholder': '0.00', 'class': 'currency-mask'}),
            'telefone_comercial': forms.TextInput(attrs={'placeholder': '(00) 0000-0000', 'class': 'phone-mask-fixo'}),
            'cep_comercial': forms.TextInput(attrs={'placeholder': '00000-000', 'class': 'cep-mask'}),
            'endereco_comercial': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'complemento_comercial': forms.TextInput(attrs={'class': 'uppercase-input'}), 
            
            # Referências
            'ref_pessoal_nome': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'ref_pessoal_telefone': forms.TextInput(attrs={'placeholder': '(00) 9.0000-0000', 'class': 'phone-mask-celular'}),
            'ref_bancaria_banco': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'ref_bancaria_agencia': forms.TextInput(),
            'ref_bancaria_conta': forms.TextInput(),

            # Condutor Adicional
            'condutor_nome': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_data_nasc': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'class': 'date-mask'}),
            'condutor_rg': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_cpf': forms.TextInput(attrs={'placeholder': '000.000.000-00', 'class': 'cpf-mask'}),
            'condutor_cnh': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_validade_cnh': forms.TextInput(attrs={'placeholder': 'DD/MM/AAAA', 'class': 'date-mask'}),
            'condutor_nome_mae': forms.TextInput(attrs={'class': 'uppercase-input'}),
            'condutor_email': forms.EmailInput(),
            'condutor_telefone': forms.TextInput(attrs={'placeholder': '(00) 9.0000-0000', 'class': 'phone-mask-celular'}),
        }
    
    # *** MÉTODO CLEAN PARA O CPF PRINCIPAL (IGNORA MÁSCARA, VALIDA ALGORITMO) ***
    def clean_cpf(self):
        """
        Limpa a máscara do CPF principal e garante que ele tenha 11 dígitos para o Model.
        Isso anula a validação de max_length do ModelForm/Model que falha com a máscara (14 digitos).
        """
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
             return cpf 
        
        cpf_limpo = re.sub(r'[^\d]', '', str(cpf)) 
        
        # Mantém a validação do algoritmo, apenas para garantir a integridade do dado.
        if not validate_cpf_algorithm(cpf_limpo):
            # Este erro só deve ocorrer se o valor original no banco for inválido.
            raise forms.ValidationError('CPF principal inválido. Contate o suporte.')
            
        return cpf_limpo 

    # *** MÉTODO CLEAN PARA O CPF/CNPJ DO CONDUTOR (IGNORA MÁSCARA, VALIDA CPF OU CNPJ) ***
    def clean_condutor_cpf(self):
        """
        Contorna a validação de max_length (11) e aplica a lógica CPF ou CNPJ (14).
        Retorna o valor limpo (somente dígitos) para o Model.
        """
        condutor_cpf = self.cleaned_data.get('condutor_cpf')
        if condutor_cpf:
            # Limpa o valor removendo pontos, traços, etc.
            cpf_cnpj_limpo = re.sub(r'[^\d]', '', str(condutor_cpf))
            
            # Validação: Verifica o tamanho e aplica a validação de algoritmo apropriada
            if len(cpf_cnpj_limpo) == 11 and not validate_cpf_algorithm(cpf_cnpj_limpo):
                raise forms.ValidationError('CPF do Condutor inválido.')
            elif len(cpf_cnpj_limpo) == 14 and not validate_cnpj_algorithm(cpf_cnpj_limpo):
                raise forms.ValidationError('CNPJ do Condutor inválido.')
            elif len(cpf_cnpj_limpo) not in (11, 14) and len(cpf_cnpj_limpo) > 0:
                 raise forms.ValidationError('CPF/CNPJ do Condutor deve ter 11 ou 14 dígitos.')
            
            return cpf_cnpj_limpo
            
        return condutor_cpf # Retorna o valor original (None ou '') se não foi preenchido