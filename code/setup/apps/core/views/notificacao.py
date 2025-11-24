from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models.notificacao import Notificacao

@login_required
def marcar_como_lida(request, pk):
    notificacao = get_object_or_404(Notificacao, pk=pk, usuario=request.user)
    
    # Marca como lida
    notificacao.lida = True
    notificacao.save()
    
    # Redireciona para o link da notificação ou para a home
    return redirect(notificacao.link if notificacao.link else '/')