from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def perfil(request):
    context = {
        'usuario': request.user
    }
    return render(request, 'usuarios/perfil.html', context)
