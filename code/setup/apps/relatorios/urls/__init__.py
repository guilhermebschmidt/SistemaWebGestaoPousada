from django.urls import path, include

app_name = 'relatorios'

urlpatterns = [
    path('', include('apps.relatorios.urls.relatorio_ocupacao')),
    path('', include('apps.relatorios.urls.relatorio_faturamento')),
]