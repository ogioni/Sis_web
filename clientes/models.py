# clientes/models.py

from django.db import models
from django.contrib.auth.models import User 

class Cliente(models.Model):
    # ----------------------------------------
    # 1. DADOS PESSOAIS (do PDF)
    # ----------------------------------------
    nome_completo = models.CharField(max_length=200, verbose_name="Nome Completo")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento", null=True, blank=True)
    rg = models.CharField(max_length=20, verbose_name="RG", blank=True, null=True)
    rg_orgao_expeditor = models.CharField(max_length=20, verbose_name="Órgão Expedidor", blank=True, null=True)
    rg_uf = models.CharField(max_length=2, verbose_name="UF RG", blank=True, null=True)
    
    # --- MUDANÇA CRÍTICA: CPF com max_length=11 ---
    cpf = models.CharField(
        max_length=11, # <-- MUDANÇA DE 14 PARA 11
        unique=True, 
        verbose_name="CPF",
        error_messages={
            'unique': "Cliente com esse CPF ja cadastrado!", 
        }
    )
    # --- FIM DA MUDANÇA ---
    
    cnh = models.CharField(max_length=20, verbose_name="Nº CNH", blank=True, null=True)
    validade_cnh = models.DateField(verbose_name="Validade CNH", null=True, blank=True)
    nome_mae = models.CharField(max_length=200, verbose_name="Nome da Mãe", blank=True, null=True)
    nome_pai = models.CharField(max_length=200, verbose_name="Nome do Pai", blank=True, null=True)
    estado_civil = models.CharField(max_length=20, verbose_name="Estado Civil", blank=True, null=True)
    
    # Contato Pessoal
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone (Fixo)", blank=True, null=True) 
    celular = models.CharField(max_length=20, verbose_name="Celular", blank=True, null=True)

    # Endereço Residencial
    cep_residencial = models.CharField(max_length=9, verbose_name="CEP Residencial", blank=True, null=True)
    endereco_residencial = models.CharField(max_length=255, verbose_name="Endereço Residencial", blank=True, null=True)
    numero_residencial = models.CharField(max_length=10, verbose_name="Nº", blank=True, null=True)
    complemento_residencial = models.CharField(max_length=100, verbose_name="Complemento", blank=True, null=True) # <--- NOVO
    bairro_residencial = models.CharField(max_length=100, verbose_name="Bairro", blank=True, null=True)
    cidade_residencial = models.CharField(max_length=100, verbose_name="Cidade", blank=True, null=True)
    estado_residencial = models.CharField(max_length=2, verbose_name="UF", blank=True, null=True)

    # ----------------------------------------
    # 2. DADOS PROFISSIONAIS
    # ----------------------------------------
    empresa = models.CharField(max_length=200, verbose_name="Empresa onde trabalha", blank=True, null=True)
    cargo = models.CharField(max_length=100, verbose_name="Cargo/Função", blank=True, null=True)
    renda_mensal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Renda Mensal", null=True, blank=True)
    telefone_comercial = models.CharField(max_length=20, verbose_name="Telefone Comercial", blank=True, null=True)
    cep_comercial = models.CharField(max_length=9, verbose_name="CEP Comercial", blank=True, null=True)
    endereco_comercial = models.CharField(max_length=255, verbose_name="Endereço Comercial", blank=True, null=True)
    complemento_comercial = models.CharField(max_length=100, verbose_name="Complemento Comercial", blank=True, null=True) # <--- NOVO

    # ----------------------------------------
    # 3. REFERÊNCIAS
    # ----------------------------------------
    ref_pessoal_nome = models.CharField(max_length=200, verbose_name="Ref. Pessoal: Nome", blank=True, null=True)
    ref_pessoal_telefone = models.CharField(max_length=20, verbose_name="Ref. Pessoal: Telefone", blank=True, null=True)
    ref_bancaria_banco = models.CharField(max_length=100, verbose_name="Ref. Bancária: Banco", blank=True, null=True)
    ref_bancaria_agencia = models.CharField(max_length=20, verbose_name="Ref. Bancária: Agência", blank=True, null=True)
    ref_bancaria_conta = models.CharField(max_length=20, verbose_name="Ref. Bancária: Conta", blank=True, null=True)

    # ----------------------------------------
    # 4. CONDUTOR ADICIONAL
    # ----------------------------------------
    condutor_nome = models.CharField(max_length=200, verbose_name="Condutor Adicional: Nome", blank=True, null=True)
    condutor_data_nasc = models.DateField(verbose_name="Condutor Adicional: Data Nasc.", null=True, blank=True)
    condutor_rg = models.CharField(max_length=20, verbose_name="Condutor Adicional: RG", blank=True, null=True)
    condutor_cpf = models.CharField(max_length=14, verbose_name="Condutor Adicional: CPF", blank=True, null=True)
    condutor_cnh = models.CharField(max_length=20, verbose_name="Nº CNH", blank=True, null=True)
    condutor_validade_cnh = models.DateField(verbose_name="Condutor Adicional: Validade CNH", null=True, blank=True)
    condutor_nome_mae = models.CharField(max_length=200, verbose_name="Condutor Adicional: Nome da Mãe", blank=True, null=True)
    condutor_email = models.EmailField(max_length=100, verbose_name="Condutor Adicional: Email", blank=True, null=True)
    condutor_telefone = models.CharField(max_length=20, verbose_name="Condutor Adicional: Telefone", blank=True, null=True)
    
    # ----------------------------------------
    # 5. CONTROLES INTERNOS
    # ----------------------------------------
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)
    tipo_pessoa = models.CharField(
        max_length=1, 
        choices=[('F', 'Pessoa Física'), ('J', 'Pessoa Jurídica')],
        default='F',
        verbose_name="Tipo"
    )
    user = models.OneToOneField(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Usuário de Acesso"
    )

    class Meta:
        verbose_name = "Cliente" 
        verbose_name_plural = "Clientes"
        ordering = ['nome_completo'] 

    def __str__(self):
        return self.nome_completo