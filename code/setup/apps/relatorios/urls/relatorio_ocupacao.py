from django.urls import path
from ..views.relatorio_ocupacao import relatorio_ocupacao

urlpatterns = [
    path('ocupacao/', relatorio_ocupacao, name='ocupacao'),
]