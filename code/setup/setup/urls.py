from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')), 
    path('', lambda request: render(request, 'index.html'), name='index'),
    path('quartos/', include('apps.core.urls.quarto')),
    path('hospedes/', include('apps.core.urls.hospede', namespace='hospede')),
    path('reservas/', include('apps.core.urls.reserva', namespace='reserva')),
    path('financeiro/', include('apps.financeiro.urls', namespace='financeiro')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('relatorios/', include('apps.relatorios.urls', namespace='relatorios')),
    path('mensalistas/', include('apps.core.urls.mensalista',namespace='mensalista')),
]