# clientes/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
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
from django.http import HttpResponseRedirect 

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
from .forms import FichaCadastralClienteForm, ClienteManutencaoForm 

# --- VIEW DE CADASTRO PÚBLICO (AQUI ESTÁ A CORREÇÃO) ---

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
                # 1. Cria a senha temporária
                senha_temporaria = get_random_string(length=12)

                # 2. Cria o User COM a senha
                user = User.objects.create_user(username=username, email=email, password=senha_temporaria)
                user.first_name = nome.split(' ')[0] 
                user.is_active = False # INATIVO (Correto)
                
                # 3. Salva
                user.save()
                
            except Exception as e:
                from django.db.utils import IntegrityError
                if isinstance(e, IntegrityError):
                    msg = "O e-mail ou CPF informado já possui cadastro."
                else:
                    msg = f"Erro desconhecido ao criar conta. ({e})"
                
                form.add_error(None, msg)
                return render(request, 'clientes/cadastro_publico_pf.html', {'form': form})

            # Se o try/except for bem-sucedido, o código continua aqui:
            novo_cliente.user = user
            novo_cliente.save() 

            #Geracao do Token e Envio do E-mail:
            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta e crie sua senha - Lider Drive'
            
            # --- CORREÇÃO APLICADA AQUI ---
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)), # MUDADO DE 'uidb64' PARA 'uid'
                'token': default_token_generator.make_token(user),
                'protocol': 'http',
                'site_name': current_site.name, # Mantido, embora o template não use
            }
            # --- FIM DA CORREÇÃO ---
            
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

# View simples para a página de sucesso
def cadastro_sucesso(request):
    return render(request, 'clientes/cadastro_sucesso.html')


# --- VIEW SEGURA PARA EDIÇÃO DE DADOS (ÁREA EXCLUSIVA) ---
class ClienteManutencaoView(LoginRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteManutencaoForm # Usa o formulário completo
    template_name = 'clientes/area_cliente.html' # O template que você já criou
    
    success_url = reverse_lazy('clientes:area_cliente') 

    def get_object(self, queryset=None):
        return get_object_or_404(Cliente, user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nome_cliente'] = self.object.nome_completo 
        return context

# --- VIEW DA ÁREA DO CLIENTE (Placeholder) ---
@login_required 
def area_cliente_logado(request):
    try:
        # Tenta carregar o formulário de manutenção
        return ClienteManutencaoView.as_view()(request)
    except Cliente.DoesNotExist:
        # Se o cliente foi criado mas o usuário ainda não está ligado a ele
        # (Isso não deve acontecer no fluxo normal)
        return render(request, 'clientes/area_cliente_erro.html')