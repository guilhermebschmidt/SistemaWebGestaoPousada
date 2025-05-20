from django.urls import path
from apps.quarto.views import quartos, index


urlpatterns = [
    path('', index, name='index'),
    path('quartos/', quartos, name='quartos' )
]