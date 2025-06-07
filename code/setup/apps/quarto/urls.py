from django.urls import path
from apps.quarto.views import (
    quartos, index, adicionar_quarto, tipos_quarto, editar_quarto, excluir_quarto,
)

app_name = 'quarto'

urlpatterns = [
    path('', index, name='index'),
    path('quartos/', quartos, name='quartos'),
    path('quartos/adicionar/', adicionar_quarto, name='adicionar_quarto'),
    path('quartos/editar/<int:quarto_id>/', editar_quarto, name='editar_quarto'),
    path('quartos/excluir/<int:quarto_id>/', excluir_quarto, name='excluir_quarto'),
    path('quartos/tipos/', tipos_quarto, name='tipos_quarto'),
]
