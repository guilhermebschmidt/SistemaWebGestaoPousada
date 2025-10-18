from django.urls import path
from ..views import relatorios as views

app_name = 'relatorios'

urlpatterns = [
    path('ocupacao/', views.relatorio_ocupacao, name='ocupacao'),   
]