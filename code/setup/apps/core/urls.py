from django.urls import path, include

urlpatterns = [
    path('hospede/', include('apps.core.urls.hospede')),
    path('quarto/', include('apps.core.urls.quarto')),
    path('reserva/', include('apps.core.urls.reserva')),
    path('reserva/<int:reserva_id>/enviar-confirmacao/', views_reserva.enviar_confirmacao_email_view, name='enviar_confirmacao_email'),
    path('relatorios/', include('apps.core.urls.relatorios', namespace='relatorios')),
]