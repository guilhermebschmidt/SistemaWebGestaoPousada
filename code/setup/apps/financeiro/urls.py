from django.urls import path, include

app_name = 'financeiro'

urlpatterns = [
    path('categoria/', include('apps.financeiro.urls.categoria')),
    path('titulo/', include('apps.financeiro.urls.titulo')),
    path('balanco/', include('apps.financeiro.urls.balanco')),
    ]
