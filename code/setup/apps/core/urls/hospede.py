from django.urls import path
from apps.core.views import hospede

app_name = 'hospede'

urlpatterns = [
    path('', hospede.listar, name='listar'),
    path('novo/', hospede.form, name='form'),
    path('buscar/', hospede.buscar, name='buscar'),
    path('<str:cpf>/', hospede.detalhes, name='detalhes'),
    path('<str:cpf>/editar/', hospede.form, name='form'),
    path('<str:cpf>/excluir/', hospede.excluir, name='excluir'),
    path('<str:cpf>/historico/', hospede.historico_hospede, name='historico'),
]