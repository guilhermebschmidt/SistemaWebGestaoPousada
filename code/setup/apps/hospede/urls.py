from django.urls import path
from . import views


urlpatterns = [
    path('', views.hospede_list, name='hospede_list'),
    path('criar/', views.hospede_create, name='hospede_create'),
    path('editar/<str:cpf>/', views.hospede_update, name='hospede_update'),
    path('deletar/<str:cpf>/', views.hospede_delete, name='hospede_delete'),
    path('buscar/', views.hospede_search, name='hospede_search'),
    path('detalhe/<str:cpf>/', views.hospede_detail, name='hospede_detail'),
]
