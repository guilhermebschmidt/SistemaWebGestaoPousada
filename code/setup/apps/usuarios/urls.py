from django.urls import path
from django.contrib.auth import views as auth_views
from .views import perfil, CustomPasswordChangeView
from .forms import CustomSetPasswordForm

urlpatterns = [
    path('perfil/', perfil, name='perfil'),
    path('change-password/', CustomPasswordChangeView.as_view(), name='account_change_password'),
     path(
        'accounts/password/reset/key/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_from_key.html', 
            form_class=CustomSetPasswordForm,             
            success_url='/accounts/password/reset/done/' 
        ),
        name='password_reset_confirm'
    ),
    path(
          'accounts/password/reset/done/',
          auth_views.PasswordResetCompleteView.as_view(
               template_name='password_reset_from_key_done.html'  # seu template de confirmação
           ),
          name='password_reset_complete'
    ),
]
