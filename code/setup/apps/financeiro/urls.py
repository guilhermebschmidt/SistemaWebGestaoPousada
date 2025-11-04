from django.urls import path, include

app_name = 'financeiro'

urlpatterns = [
    path('categoria/', include('apps.financeiro.urls.categoria')),
    path('titulo/', include('apps.financeiro.urls.titulo')),
    path('relatorio/', include('apps.financeiro.urls.relatorio_faturamento')), 
    ]
