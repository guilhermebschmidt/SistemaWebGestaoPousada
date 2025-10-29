from django.urls import path
from apps.financeiro.views.titulo import list_titulos, titulo_form, marcar_pago

app_name = 'financeiro'

urlpatterns = [
    path('', list_titulos, name='list_titulos'),
    path('novo/', titulo_form, name='novo_titulo'),
    path('<int:pk>/editar/', titulo_form, name='editar_titulo'),
    path('<int:pk>/marcar_pago/', marcar_pago, name='marcar_pago'),
]
