from django.urls import path
from ..views import notificacao

app_name = 'notificacao'

urlpatterns = [
    path('ler/<int:pk>/', notificacao.marcar_como_lida, name='marcar_como_lida'),
]