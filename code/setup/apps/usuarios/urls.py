from django.urls import path
from django.contrib.auth import views as auth_views
from .views import perfil, CustomPasswordChangeView
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('perfil/', perfil, name='perfil'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='account_change_password'),
    
]
