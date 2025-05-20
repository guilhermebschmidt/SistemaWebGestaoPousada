from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: render(request, 'index.html'), name='index'),
    path('quartos/', include('apps.quarto.urls')),
    path('hospedes/', include('apps.hospede.urls')),
]