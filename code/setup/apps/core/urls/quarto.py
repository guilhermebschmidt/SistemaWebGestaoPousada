from django.urls import path
import apps.core.views.quarto as quarto

urlpatterns = [
    path('', quarto.index, name='index'),
    path('quartos/', quarto.quartos, name='quartos'),
    path('quartos/form/', quarto.form, name='form'),  # Para adicionar
    path('quartos/form/<int:quarto_id>/', quarto.form, name='form'),  # Para editar
    path('quartos/excluir/<int:quarto_id>/', quarto.excluir_quarto, name='excluir_quarto'),
    path('quartos/tipos/', quarto.tipos_quarto, name='tipos_quarto'),
]