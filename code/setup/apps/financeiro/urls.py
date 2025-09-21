from django.urls import path, include

urlpatterns = [
    path('titulo/', include('apps.financeiro.urls.titulo')),
]