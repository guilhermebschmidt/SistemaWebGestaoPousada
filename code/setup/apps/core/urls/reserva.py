from django.urls import path
import apps.core.views.reserva as reserva

app_name = 'reserva'

urlpatterns = [
    path('', reserva.list, name='list'),
    path('checkin/', reserva.list_checkin, name = 'list_checkin'),
    path('novo/', reserva.add, name='form'),
    path('<int:pk>/editar/', reserva.update, name='update'),
    path('<int:pk>/excluir/', reserva.delete, name='delete'),
    path('buscar/', reserva.search, name='search'),
]