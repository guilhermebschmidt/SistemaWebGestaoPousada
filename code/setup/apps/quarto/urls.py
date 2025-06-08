from django.urls import path
from apps.quarto.views import (
    quartos, index, form, tipos_quarto, excluir_quarto,
)

app_name = 'quarto'

urlpatterns = [
    path('', index, name='index'),
    path('quartos/', quartos, name='quartos'),
    path('quartos/form/', form, name='form'),  # Para adicionar
    path('quartos/form/<int:quarto_id>/', form, name='form'),  # Para editar
    path('quartos/excluir/<int:quarto_id>/', excluir_quarto, name='excluir_quarto'),
    path('quartos/tipos/', tipos_quarto, name='tipos_quarto'),
]