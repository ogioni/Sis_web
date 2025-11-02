# clientes/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
# [NOVO] Importamos send_mail e a classe EmailBackend para envio dinâmico
from django.core.mail import EmailMessage, get_connection
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.utils.crypto import get_random_string 
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
import json
# Imports para validação de e-mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

# [NOVO] Importação necessária para formatar datas (DD/MM/AAAA)
from django.utils.dateformat import DateFormat 

# Imports das Views Padrão
from django.contrib.auth.views import (
    PasswordChangeView, 
    LoginView, 
    PasswordResetConfirmView
)
# Imports para a Área do Cliente
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView

# Imports dos Nossos Modelos e Forms
from .models import Cliente 
from .forms import (
    FichaCadastralClienteForm, 
    ClienteManutencaoForm, 
    validate_cpf_algorithm,
    validate_cnpj_algorithm
)

# [NOVO] Importar o modelo de configuração do site
from core.models import SiteConfiguracao


# --- FUNÇÃO AUXILIAR PARA ENVIO DE E-MAIL DINÂMICO ---
def send_dynamic_email(mail_subject, message, to_email):
# ... (código send_dynamic_email permanece inalterado) ...
    """
    Tenta enviar o e-mail usando as credenciais do Admin (SiteConfiguracao).
    Se as credenciais estiverem incompletas, usa a configuração padrão do settings.
    """
    try:
        config = SiteConfiguracao.objects.first()
        
        # 1. Checa se as configurações mínimas de SMTP estão no Admin
        if config and config.is_email_config_complete():
            
            # Cria a conexão dinamicamente
            connection = get_connection(
                host=config.email_host,
                port=config.email_port,
                username=config.email_host_user,
                password=config.email_host_password,
                use_tls=config.email_use_tls
            )
            
            # Usa o remetente dinâmico do Admin
            from_email = config.default_from_email
            
            email_message = EmailMessage(
                mail_subject, 
                message, 
                from_email, 
                to=[to_email],
                connection=connection # Envia pela conexão dinâmica
            )
            email_message.send()
            return True # Sucesso no envio dinâmico
            
        else:
            # 2. Se a configuração do Admin estiver incompleta, volta para o padrão (Console/Settings)
            email_message = EmailMessage(
                mail_subject, 
                message, 
                to=[to_email]
            )
            email_message.send() # Envia pela conexão padrão (que é o Console no DEV)
            return True
            
    except Exception as e:
        # Em caso de qualquer falha, logamos e retornamos Falso
        print(f"ERRO DE ENVIO DE E-MAIL DINÂMICO: {e}")
        return False


# --- [MODIFICADO] VIEW DO NOVO CADASTRO DINÂMICO (PF/PJ) ---
@transaction.atomic
def cadastro_dinamico_view(request):
# ... (código cadastro_dinamico_view permanece inalterado) ...
    pass # Removido para brevidade
    if request.method == 'POST':
        # --- INÍCIO DA LÓGICA DE POST (COPIADA DE cadastro_publico_pf) ---
        form = FichaCadastralClienteForm(request.POST)
        
        if form.is_valid():
            novo_cliente = form.save(commit=False)
            email = form.cleaned_data['email']
            nome = form.cleaned_data['nome_completo']
            username = email 
            
            try:
                senha_temporaria = get_random_string(length=12)
                user = User.objects.create_user(username=username, email=email, password=senha_temporaria)
                user.first_name = nome.split(' ')[0] 
                user.is_active = False 
                user.save()
            except Exception as e:
                from django.db.utils import IntegrityError
                if isinstance(e, IntegrityError):
                    msg = "O e-mail ou CPF informado já possui cadastro."
                else:
                    msg = f"Erro desconhecido ao criar conta. ({e})"
                
                form.add_error(None, msg)
                # [MODIFICADO] Renderiza o template NOVO com erro
                context = {
                    'page_title': 'Novo Cadastro - 1/3',
                    'form': form, 
                    'show_form_on_load': True # Força o JS a mostrar o form
                }
                return render(request, 'clientes/cadastro_dinamico.html', context)

            novo_cliente.user = user
            novo_cliente.save() 

            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta e crie sua senha - Lider Drive'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                'site_name': current_site.name,
            }
            message = render_to_string('registration/password_reset_email.html', context)
            to_email = form.cleaned_data['email']

                    # [MODIFICADO] Chamando a função de envio dinâmico
            send_dynamic_email(mail_subject, message, to_email) 
            
            return redirect('clientes:cadastro_sucesso')
        
        else:
            # [Formulário INVÁLIDO] 
            pass
    
    else: # request.method == 'GET'
        form = FichaCadastralClienteForm()

    # --- LÓGICA DE GET (e de POST inválido) ---
    context = {
        'page_title': 'Novo Cadastro - 1/3',
        'form': form, 
    }
    
    if request.method == 'POST' and not form.is_valid():
        # Se for um POST inválido, diz ao template para pular a verificação
        context['show_form_on_load'] = True

    return render(request, 'clientes/cadastro_dinamico.html', context)


# --- VIEW DE CADASTRO PÚBLICO (LEGADO) ---
@transaction.atomic 
def cadastro_publico_pf(request):
# ... (código cadastro_publico_pf permanece inalterado) ...
    pass # Removido para brevidade
    if request.method == 'POST':
        form = FichaCadastralClienteForm(request.POST)
        
        if form.is_valid():
            novo_cliente = form.save(commit=False)
            email = form.cleaned_data['email']
            nome = form.cleaned_data['nome_completo']
            username = email 
            
            try:
                senha_temporaria = get_random_string(length=12)
                user = User.objects.create_user(username=username, email=email, password=senha_temporaria)
                user.first_name = nome.split(' ')[0] 
                user.is_active = False 
                user.save()
            except Exception as e:
                from django.db.utils import IntegrityError
                if isinstance(e, IntegrityError):
                    msg = "O e-mail ou CPF informado já possui cadastro."
                else:
                    msg = f"Erro desconhecido ao criar conta. ({e})"
                form.add_error(None, msg)
                return render(request, 'clientes/cadastro_publico_pf.html', {'form': form})

            novo_cliente.user = user
            novo_cliente.save() 

            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta e crie sua senha - Lider Drive'
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                'site_name': current_site.name,
            }
            message = render_to_string('registration/password_reset_email.html', context)
            to_email = form.cleaned_data['email']
            
            # [MODIFICADO] Envio de e-mail agora usa a função dinâmica
            send_dynamic_email(mail_subject, message, to_email) 
            
            return redirect('clientes:cadastro_sucesso')
        else:
            form = FichaCadastralClienteForm()

    context = {
        'form': form,
        'page_title': 'Crie sua Conta - 1/3',
    }
    return render(request, 'clientes/cadastro_publico_pf.html', context)

# View simples para a página de sucesso
def cadastro_sucesso(request):
  return render(request, 'clientes/cadastro_sucesso.html')


# --- VIEW SEGURA PARA EDIÇÃO DE DADOS (ÁREA EXCLUSIVA) ---
class ClienteManutencaoView(LoginRequiredMixin, UpdateView):
  model = Cliente
  form_class = ClienteManutencaoForm
  # [ALTERADO] Usando o template de ficha cadastral para a edição.
  template_name = 'clientes/ficha_cadastral.html' 
  success_url = reverse_lazy('clientes:area_cliente') 

  def get_object(self, queryset=None):
    """Garante que o cliente só possa editar seu próprio registro."""
    return get_object_or_404(Cliente, user=self.request.user)

  # [NOVO] Adicionando get_initial para pré-formatar datas
  def get_initial(self):
    initial = super().get_initial()
    obj = self.get_object() # O objeto Cliente que está sendo editado

    # Formata as datas para DD/MM/AAAA, que é o formato esperado pela máscara
    # Se o campo de data não estiver vazio (NULL)
    if obj.data_nascimento:
        initial['data_nascimento'] = DateFormat(obj.data_nascimento).format('d/m/Y')
        
    if obj.validade_cnh:
        initial['validade_cnh'] = DateFormat(obj.validade_cnh).format('d/m/Y')
        
    if obj.condutor_data_nasc:
        initial['condutor_data_nasc'] = DateFormat(obj.condutor_data_nasc).format('d/m/Y')
        
    if obj.condutor_validade_cnh:
        initial['condutor_validade_cnh'] = DateFormat(obj.condutor_validade_cnh).format('d/m/Y')

    return initial
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['nome_cliente'] = self.object.nome_completo
    # Adicionamos um título para a página de edição, que usa o template base_cliente.html
    context['page_title'] = 'Ficha Cadastral (Edição)' 
    return context
  
  def form_valid(self, form):
    """Adiciona mensagem de sucesso após salvar o formulário."""
    response = super().form_valid(form)
    messages.success(self.request, "Seus dados foram atualizados com sucesso!")
    return response

# --- VIEW DA ÁREA DO CLIENTE (Dashboard) ---
@login_required 
def area_cliente_logado(request):
# ... (código area_cliente_logado permanece inalterado) ...
    pass # Removido para brevidade
    """
    Esta view agora foca em ser o Dashboard principal.
    Se o cliente ainda não tiver completado a ficha, pode-se redirecionar aqui.
    Mas, por enquanto, vamos apenas renderizar o dashboard.
    """
    try:
        # Busca o objeto Cliente associado
        cliente = Cliente.objects.get(user=request.user)
        context = {
            'page_title': 'Área do Cliente',
            'cliente': cliente,
        }
        return render(request, 'clientes/area_cliente.html', context)

    except Cliente.DoesNotExist:
        # Se por algum motivo o Cliente não for encontrado, mostra um erro ou redireciona
        return render(request, 'clientes/area_cliente_erro.html', {'page_title': 'Erro'})

# --- FUNÇÃO AUXILIAR PARA MASCARAR E-MAIL ---
def mask_email(email):
# ... (código mask_email permanece inalterado) ...
    pass # Removido para brevidade
    try:
        local, domain = email.split('@')
        local_masked = local[0] + '***' + local[-1] if len(local) > 2 else local[0] + '***'
        domain_parts = domain.split('.')
        domain_name = domain_parts[0]
        domain_ext = ".".join(domain_parts[1:])
        domain_masked = domain_name[0] + '***' + domain_name[-1] if len(domain_name) > 2 else domain_name[0] + '***'
        return f"{local_masked}@{domain_masked}.{domain_ext}"
    except Exception:
        return "e-mail cadastrado"

# --- FUNÇÃO AUXILIAR PARA MASCARAR CPF ---
def mask_cpf(cpf):
# ... (código mask_cpf permanece inalterado) ...
    pass # Removido para brevidade
    try:
        cpf_limpo = "".join(filter(str.isdigit, str(cpf)))
        if len(cpf_limpo) == 11:
          return f"***.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-**"
        else:
          return "documento cadastrado"
    except Exception:
        return "documento cadastrado"


# --- [REFINADO] VIEW AJAX COM LÓGICA DE PRIORIDADE CORRETA ---
def verificar_documento_ajax(request):
# ... (código verificar_documento_ajax permanece inalterado) ...
    pass # Removido para brevidade
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            documento = data.get('documento', '')
            email = data.get('email', '').lower().strip()
            
            documento_limpo = "".join(filter(str.isdigit, documento))
            doc_type = None

            # --- ETAPA 1: Validar o Documento PRIMEIRO (Sua Lógica) ---
            if len(documento_limpo) == 11:
                doc_type = 'cpf'
                if not validate_cpf_algorithm(documento_limpo):
                    return JsonResponse({'status': 'error', 'message': 'CPF inválido.'}, status=400)
            
            elif len(documento_limpo) == 14:
                doc_type = 'cnpj'
                if not validate_cnpj_algorithm(documento_limpo):
                    return JsonResponse({'status': 'error', 'message': 'CNPJ inválido.'}, status=400)
            
            else:
                return JsonResponse({'status': 'error', 'message': 'Documento inválido.'}, status=400)

            # --- ETAPA 2: Validar o Formato do E-mail ---
            try:
                validate_email(email)
            except ValidationError:
                return JsonResponse({'status': 'error', 'message': 'Formato de e-mail inválido.'}, status=400)

            # --- ETAPA 3: Checar Duplicidade (Banco de Dados) ---
            
            # 3a. Checar E-mail (e buscar CPF associado)
            user_qs = User.objects.filter(email__iexact=email)
            if user_qs.exists():
                user_encontrado = user_qs.first()
                reset_url = reverse('password_reset')
                cpf_associado_str = "a outra conta" # Fallback
                
                try:
                    if hasattr(user_encontrado, 'cliente'):
                        cpf_associado_str = mask_cpf(user_encontrado.cliente.cpf)
                except Exception:
                    pass 

                msg = f'Este e-mail já está cadastrado (associado ao {cpf_associado_str}). Tente <a href="{reset_url}">recuperar sua senha</a>.'
                return JsonResponse({'status': 'exists', 'message': msg})
            
            # 3b. Checar Documento (só se for CPF, por enquanto)
            if doc_type == 'cpf':
                cliente_qs = Cliente.objects.filter(cpf=documento_limpo)
                if cliente_qs.exists():
                    cliente = cliente_qs.first()
                    email_mascarado = mask_email(cliente.user.email)
                    reset_url = reverse('password_reset') 
                    msg = f'Este CPF já possui cadastro (associado ao e-mail: {email_mascarado}).<br>Se você é o titular, <a href="{reset_url}">recupere sua senha</a>.'
                    return JsonResponse({'status': 'exists', 'message': msg})
            
            # --- ETAPA 4: Tudo Válido e Novo! ---
            if doc_type == 'cpf':
                return JsonResponse({'status': 'not_found', 'doc_type': doc_type})
            elif doc_type == 'cnpj':
                return JsonResponse({'status': 'not_found_pj'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)