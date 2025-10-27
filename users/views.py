#user/views.py 

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
from django.http import HttpResponseRedirect # Necessário para redirecionamento após salvar

# Imports das Views Padrão
from django.contrib.auth.views import (
    PasswordChangeView, 
    LoginView, 
    PasswordResetConfirmView
)

# Imports dos Nossos Modelos e Forms
from clientes.models import Cliente
from clientes.forms import FichaCadastralClienteForm 

# --- NOSSAS VIEWS DE LOGIN E TROCA FORÇADA (JÁ FUNCIONANDO) ---

class MinhaLoginView(LoginView):
    # Esta view está ligada a /contas/login/, que não estamos usando como principal
    template_name = 'paginas/login.html' 
    redirect_authenticated_user = True
    # next_page = reverse_lazy('admin:index')

class MinhaPasswordChangeView(PasswordChangeView):
    template_name = 'paginas/change_password.html' # (A tela de troca forçada)
    success_url = reverse_lazy('admin:index') 

    def form_valid(self, form):
        # Remove o usuário do grupo de bloqueio
        try:
            usuario = self.request.user
            grupo = Group.objects.get(name='Deve Mudar Senha')
            usuario.groups.remove(grupo)
        except Group.DoesNotExist:
            pass
        return super().form_valid(form)


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
                user = User.objects.create_user(username=username, email=email)
                user.first_name = nome.split(' ')[0] 
                user.is_active = False # INATIVO (Correto)
                user.set_unusable_password() 
                user.save()
            except Exception as e:
                form.add_error(None, f"Erro ao criar conta de usuário. Verifique os dados.")
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

# View simples para a página de sucesso
def cadastro_sucesso(request):
    return render(request, 'clientes/cadastro_sucesso.html')


# --- VIEW DE CONFIRMAÇÃO CORRIGIDA (PASSO 448) ---

class MinhaPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'
    success_url = reverse_lazy('admin:login') 

    # (Req 2) Mostra o nome do cliente na tela
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if hasattr(self, 'user') and self.user is not None:
            try:
                cliente = Cliente.objects.get(user=self.user)
                context['nome_completo'] = cliente.nome_completo 
            except Cliente.DoesNotExist:
                context['nome_completo'] = self.user.username 
        
        return context

    # (Req 1) Ativa o usuário quando a senha for criada
    def form_valid(self, form):
        # --- A CORREÇÃO LÓGICA ESTÁ AQUI ---
        
        # 1. Pega o usuário (self.user) que a view PAI (PasswordResetConfirmView) 
        #    já validou através do link (uid e token)
        user = self.user 
        
        # 2. ATIVA O USUÁRIO (TICKET VERDE)
        user.is_active = True
        user.save()

        # 3. Agora que o usuário está ativo,
        #    chama a função do formulário para salvar a nova senha
        form.save() # Salva a nova senha
        
        # 4. Redireciona manualmente para a URL de sucesso
        return HttpResponseRedirect(self.get_success_url())
        # --- FIM DA CORREÇÃO ---