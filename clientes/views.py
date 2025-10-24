from django.shortcuts import render, redirect
from .models import Cliente
from .forms import FichaCadastralClienteForm # Novo nome para o form de registro simples

def cadastro_publico_pf(request):
    if request.method == 'POST':
        form = FichaCadastralClienteForm(request.POST)
        if form.is_valid():
            # A lógica para salvar o cliente E criar o usuário virá aqui
            # Por enquanto, só redirecionamos
            return redirect('clientes:cadastro_sucesso') 
    else:
        form = FichaCadastralClienteForm()

    context = {
        'form': form,
        'page_title': 'Crie sua conta - Lider Drive',
    }
    return render(request, 'clientes/cadastro_publico_pf.html', context)

def cadastro_sucesso(request):
    # Esta view será o ponto onde informamos sobre o email de validação
    return render(request, 'clientes/cadastro_sucesso.html')