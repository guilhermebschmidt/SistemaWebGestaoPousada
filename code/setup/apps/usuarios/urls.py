from django.urls import path, include
from . import views

urlpatterns = [
     path('accounts/', include('allauth.urls')),
     path('perfil/', views.perfil, name='perfil'),
]