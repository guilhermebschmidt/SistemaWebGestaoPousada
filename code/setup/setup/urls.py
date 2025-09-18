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

]