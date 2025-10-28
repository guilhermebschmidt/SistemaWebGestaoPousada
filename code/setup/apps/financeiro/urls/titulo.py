from django.urls import path
from apps.financeiro.views.titulo import list_titulos, titulo_form, marcar_pago

app_name = 'financeiro'

urlpatterns = [
    path('titulos/', list_titulos, name='list_titulos'),
    path('titulos/novo/', titulo_form, name='novo_titulo'),
    path('titulos/<int:titulo_id>/editar/', titulo_form, name='editar_titulo'),
    path('titulos/<int:titulo_id>/marcar_pago/', marcar_pago, name='marcar_pago'),
]
