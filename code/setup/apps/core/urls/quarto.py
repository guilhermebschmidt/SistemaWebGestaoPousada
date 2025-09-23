from django.urls import path
import apps.core.views.quarto as quarto

app_name = 'quarto'

urlpatterns = [
    path('', quarto.listar , name='listar'),  # esse será /quartos/
    path('form/', quarto.form, name='form'),
    path('form/<int:quarto_id>/', quarto.form, name='form'),
    path('excluir/<int:quarto_id>/', quarto.excluir, name='excluir'),
    path('tipos/', quarto.tipos_quarto, name='tipos_quarto'),
]