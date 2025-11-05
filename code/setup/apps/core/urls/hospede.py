from django.urls import path
from apps.core.views import hospede

app_name = 'hospede'

# Rotas originais mantidas; adicionamos aliases/param names compatíveis com os testes
urlpatterns = [
    path('', hospede.listar, name='listar'),
    # criação: rota legada e alias 'form' esperado pelos testes
    path('novo/', hospede.hospede_form, name='criar'),
    path('form/', hospede.hospede_form, name='form'),
    # busca
    path('buscar/', hospede.buscar, name='buscar'),
    # detalhes/editar/excluir/historico usando 'cpf' como nome de parâmetro para casar com os testes
    path('<str:cpf>/', hospede.detalhes, name='detalhes'),
    path('<str:cpf>/editar/', hospede.hospede_form, name='editar'),
    path('<str:cpf>/form/', hospede.hospede_form, name='form'),
    path('<str:cpf>/excluir/', hospede.excluir, name='excluir'),
    path('<str:cpf>/historico/', hospede.historico_hospede, name='historico'),
]