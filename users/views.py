from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group

# Esta é a nossa "View". Estamos herdando (usando) a lógica pronta do Django
# e apenas dizendo a ela 2 coisas: qual template usar e para onde ir depois.

class MinhaPasswordChangeView(PasswordChangeView):

    # 1. Diga ao Django para usar o nosso HTML personalizado
    template_name = 'paginas/mudar_senha.html'

    # 2. Diga ao Django para onde redirecionar o usuário DEPOIS 
    #    que ele mudar a senha com sucesso.
    #    Vamos mandá-lo para o painel de admin por enquanto.
    success_url = reverse_lazy('admin:index')

    # 2. ADICIONE TODO O MÉTODO ABAIXO
    def form_valid(self, form):
        # Este método é chamado QUANDO o formulário é válido,
        # ANTES de salvar a senha e redirecionar.

        try:
            # Pega o usuário que está logado
            usuario = self.request.user

            # Pega o grupo de bloqueio
            grupo = Group.objects.get(name='Deve Mudar Senha')

            # Remove o usuário do grupo!
            usuario.groups.remove(grupo)

        except Group.DoesNotExist:
            # Se o grupo não existir, não faz nada
            pass

        # Continua com o processo normal de salvar a senha
        return super().form_valid(form)