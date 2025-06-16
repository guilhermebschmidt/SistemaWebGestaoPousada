from django.urls import path
import apps.core.views.quarto as quarto


urlpatterns = [
    path('', quarto.quartos, name='quartos'),  # esse será /quartos/
    path('form/', quarto.form, name='form'),
    path('form/<int:quarto_id>/', quarto.form, name='form'),
    path('excluir/<int:quarto_id>/', quarto.excluir_quarto, name='excluir_quarto'),
    path('tipos/', quarto.tipos_quarto, name='tipos_quarto'),
]