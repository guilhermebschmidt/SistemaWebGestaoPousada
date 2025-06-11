from django.urls import path
import apps.core.views.hospede as hospede

urlpatterns = [
    path('', hospede.hospede_list, name='hospede_list'),
    path('novo/', hospede.hospede_create, name='hospede_create'),
    path('<str:cpf>/', hospede.hospede_detail, name='hospede_detail'),
    path('<str:cpf>/editar/', hospede.hospede_update, name='hospede_update'),
    path('<str:cpf>/excluir/', hospede.hospede_delete, name='hospede_delete'),
    path('buscar/', hospede.hospede_search, name='hospede_search'),
]