from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator # Gerador de token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse

from .models import Cliente
from .forms import FichaCadastralClienteForm # Nosso formulário da Fase 1

def cadastro_publico_pf(request):
    if request.method == 'POST':
        # 1. Pega os dados enviados
        form = FichaCadastralClienteForm(request.POST)
        
        if form.is_valid():
            # 2. O formulário (forms.py) já validou CPF, E-mail duplicado, etc.
            
            # 3. Cria o Cliente (mas não salva no banco ainda)
            novo_cliente = form.save(commit=False)
            
            # 4. Cria o Usuário (User)
            email = form.cleaned_data['email']
            nome = form.cleaned_data['nome_completo']
            
            # Define um username (pode ser o email ou parte dele)
            # Vamos usar o email como username para garantir que seja único
            username = email 
            
            try:
                # Cria o usuário. Ele fica INATIVO por padrão (is_active=False)
                # e sem senha definida (set_unusable_password)
                user = User.objects.create_user(username=username, email=email)
                user.is_active = False
                user.first_name = nome.split(' ')[0] # Pega o primeiro nome
                user.set_unusable_password() # Força o usuário a NÃO conseguir logar
                user.save()
            except Exception as e:
                # Se der erro ao criar o usuário (ex: username duplicado, raro)
                form.add_error(None, f"Erro ao criar conta de usuário: {e}")
                return render(request, 'clientes/cadastro_publico_pf.html', {'form': form})

            # 5. Liga o Cliente ao Usuário recém-criado
            novo_cliente.user = user
            novo_cliente.save() # Agora salva o cliente no banco

            # 6. Envia o E-mail de Ativação/Criação de Senha
            current_site = get_current_site(request)
            mail_subject = 'Ative sua conta e crie sua senha - Lider Drive'
            
            # Monta o contexto para o template do e-mail
            context = {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
                'protocol': 'http', # Em produção, mudamos para 'https'
            }
            
            # Renderiza o template do e-mail (que vamos criar)
            message = render_to_string('registration/activation_email.html', context)
            
            to_email = form.cleaned_data['email']
            email_message = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email_message.send() # Envia (para o console, por enquanto)

            # 7. Redireciona para a página de sucesso
            return redirect('clientes:cadastro_sucesso')
    
    else:
        # Se for o primeiro acesso (GET), mostra o formulário vazio
        form = FichaCadastralClienteForm()

    context = {
        'form': form,
        'page_title': 'Crie sua Conta - Lider Drive',
    }
    return render(request, 'clientes/cadastro_publico_pf.html', context)

# View simples para a página de sucesso
def cadastro_sucesso(request):
    return render(request, 'clientes/cadastro_sucesso.html')

# --- PRÓXIMOS PASSOS (Views de Ativação) ---
# (Vamos adicionar a view de ativação e criação de senha depois)