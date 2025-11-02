from django.urls import path
from .views import perfil, CustomPasswordChangeView

urlpatterns = [
    path('perfil/', perfil, name='perfil'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='account_change_password'),    
]
