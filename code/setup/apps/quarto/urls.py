from django.urls import path
from apps.quarto.views import quartos, index, adicionar_quarto, tipos_quarto

app_name = 'quarto'

urlpatterns = [
    path('', index, name='index'),
    path('quartos/', quartos, name='quartos'),
    path('quartos/adicionar/', adicionar_quarto, name='adicionar_quarto'),
    path('quartos/tipos/', tipos_quarto, name='tipos_quarto'),
]
