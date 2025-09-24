from django.shortcuts import render
from allauth.account.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import CustomChangePasswordForm

def perfil(request):
    context = {
        'usuario': request.user
    }
    return render(request, 'usuarios/perfil.html', context)

#redicionamento pós alteração da senha com sucesso
class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomChangePasswordForm
    success_url = reverse_lazy('perfil')