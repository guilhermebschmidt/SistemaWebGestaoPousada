from django.urls import path
from . import views

app_name = 'relatorios'

urlpatterns = [
    path('ocupacao/', views.relatorio_ocupacao, name='ocupacao'),   
]