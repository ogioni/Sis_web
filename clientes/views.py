from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.db import transaction
from django.utils.crypto import get_random_string
from django.contrib import messages

# --- NOVOS IMPORTS PARA A ÁREA DO CLIENTE ---
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
# --- FIM DOS NOVOS IMPORTS ---

from .models import Cliente
# Importa OS DOIS formulários
from .forms import FichaCadastralClienteForm, ClienteManutencaoForm 

# --- VIEW DE CADASTRO PÚBLICO (JÁ FUNCIONANDO) ---
@transaction.atomic 
def cadastro_publico_pf(request):
    if request.method == 'POST':
        form = FichaCadastralClienteForm(request.POST)
        
        if form.is_valid():
            novo_cliente = form.save(commit=False)
            email = form.cleaned_data['email']
            nome = form.cleaned_data['nome_completo']
            username = email 
            
            try:
                # 1. Cria a senha temporária para garantir que o User tenha credenciais.
                # from django.contrib.auth.models import User
                senha_temporaria = get_random_string(length=12)

                # 2. Cria o User COM a senha
                user = User.objects.create_user(username=username, email=email, password=senha_temporaria)
                user.first_name = nome.split(' ')[0] 
                user.is_active = False # INATIVO (Correto)
                
                #3. Salva explicitamente e força o PK a existir
                user.save()
                
            except Exception as e:
                # Se for um erro de duplicidade (IntegrityError)
                from django.db.utils import IntegrityError
                
                if isinstance(e, IntegrityError):
                    # Tenta dar uma mensagem mais específica
                    msg = "O e-mail ou CPF informado já possui cadastro."
                else:
                    # Mensagem genérica com o erro real no console
                    msg = f"Erro desconhecido ao criar conta. ({e})"
                
                form.add_error(None, msg)
                return render(request, 'clientes/cadastro_publico_pf.html', {'form': form})

            # Se o try/except for bem-sucedido, o código continua aqui:
            novo_cliente.user = user
            novo_cliente.save() 

            #Geracao do Token e Envio do E-mail:
            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta e crie sua senha - Lider Drive'
            context = {
                'user': user,
                'domain': current_site.domain,
                # uidb64 Correto
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                'site_name': current_site.name,
            }
            
            message = render_to_string('registration/password_reset_email.html', context)
            to_email = form.cleaned_data['email']
            email_message = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email_message.send() # Envia para o console

            return redirect('clientes:cadastro_sucesso')
    
    else:
        form = FichaCadastralClienteForm()

    context = {
        'form': form,
        'page_title': 'Crie sua Conta - 1/3',
    }
    return render(request, 'clientes/cadastro_publico_pf.html', context)

@login_required # Garante que só quem está logado pode entrar
def area_cliente_logado(request):
    # Retorna o template que você já criou (area_cliente.html)
    return render(request, 'clientes/area_cliente.html', {'user': request.user})


# View simples para a página de sucesso
def cadastro_sucesso(request):
    return render(request, 'clientes/cadastro_sucesso.html')


# --- PASSO 455: NOVA VIEW SEGURA PARA EDIÇÃO DE DADOS (ÁREA EXCLUSIVA) ---

# LoginRequiredMixin garante que só usuários logados acessem
class ClienteManutencaoView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteManutencaoForm # Usa o formulário completo
    template_name = 'clientes/area_cliente.html' # O template que você já criou
    
    # Para onde ir após salvar com sucesso? De volta para a mesma página.
    success_url = reverse_lazy('clientes:area_cliente') 

    # 1. GARANTIA DE SEGURANÇA: Esta é a função mais importante.
    # Ela garante que o usuário logado (request.user) só possa
    # editar o objeto Cliente que está ligado a ele.
    def get_object(self, queryset=None):
        # Busca o objeto 'Cliente' que tenha o campo 'user'
        # igual ao usuário que está logado (self.request.user).
        # Se ele tentar acessar o 'Cliente' de outro usuário, dará erro 404.
        return get_object_or_404(Cliente, user=self.request.user)

    # 2. (Opcional) Adiciona dados extras ao template
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 'object' é o nome padrão que a UpdateView dá ao item sendo editado
        context['nome_cliente'] = self.object.nome_completo 
        return context