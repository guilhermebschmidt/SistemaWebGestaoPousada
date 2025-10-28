from django.urls import path, include

urlpatterns = [
    path('hospede/', include('apps.core.urls.hospede')),
    path('quarto/', include('apps.core.urls.quarto')),
    path('reserva/', include('apps.core.urls.reserva')),
    path('mensalista/', include('apps.core.urls.mensalista')),
]
