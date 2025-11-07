from django.urls import path
from apps.financeiro.views.titulo import list_titulos, titulo_form, marcar_pago

app_name = 'financeiro'

urlpatterns = [
    # rota principal (alias 'list' esperado nos testes)
    path('', list_titulos, name='list_titulos'),
    path('', list_titulos, name='list'),
    # formulário de criação/edição (alias 'form' e 'update' esperados nos testes)
    path('novo/', titulo_form, name='novo_titulo'),
    path('form/', titulo_form, name='form'),
    path('<int:pk>/editar/', titulo_form, name='editar_titulo'),
    path('<int:pk>/update/', titulo_form, name='update'),
    path('<int:pk>/marcar_pago/', marcar_pago, name='marcar_pago'),
]
