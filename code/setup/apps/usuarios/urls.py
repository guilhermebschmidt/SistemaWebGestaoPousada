from django.urls import path, include
from .views import perfil, CustomPasswordChangeView

urlpatterns = [
     path('accounts/', include('allauth.urls')),
     path('perfil/', perfil, name='perfil'),
     path('change-password/', CustomPasswordChangeView.as_view(), name='account_change_password'),

]