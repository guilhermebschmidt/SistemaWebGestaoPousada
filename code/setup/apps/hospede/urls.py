from django.urls import path
from . import views

app_name = 'hospede'

urlpatterns = [
    path('', views.hospede_list, name='hospede_list'),
    path('novo/', views.hospede_create, name='hospede_create'),
    path('<str:cpf>/', views.hospede_detail, name='hospede_detail'),
    path('<str:cpf>/editar/', views.hospede_update, name='hospede_update'),
    path('<str:cpf>/excluir/', views.hospede_delete, name='hospede_delete'),
    path('buscar/', views.hospede_search, name='hospede_search'),
]