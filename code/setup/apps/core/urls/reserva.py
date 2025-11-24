from django.urls import path
import apps.core.views.reserva as reserva

app_name = 'reserva'

urlpatterns = [
    path('', reserva.list, name='list'),
    path('checkin/', reserva.list_checkin, name = 'list_checkin'),
    path('checkout/', reserva.list_checkout, name = 'list_checkout'),
    path('novo/', reserva.reserva_form, name='criar'),
    path('<int:pk>/editar/', reserva.reserva_form, name='editar'),
    path('<int:pk>/excluir/', reserva.cancelar_reserva, name='cancelar'),
    path('buscar/', reserva.search, name='search'),
    path('<int:pk>/checkin/', reserva.marcar_checkin, name='checkin'),
    path('<int:pk>/checkout/', reserva.marcar_checkout, name='checkout'),
    path('buscar-hospedes/', reserva.buscar_hospedes, name='buscar_hospedes'),
    path('<int:reserva_id>/enviar-confirmacao/', reserva.enviar_confirmacao_email_view, name='enviar_confirmacao_email'),
]