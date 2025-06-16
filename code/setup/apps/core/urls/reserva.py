from django.urls import path
import apps.core.views.reserva as reserva

app_name = 'reserva'

urlpatterns = [
    path('', reserva.list, name='list'),
    path('', reserva.list_checkin, name = 'list_checkin'),
    path('novo/', reserva.add, name='form'),
    #path('<str:cpf>/', reserva.details, name='details'),
    #path('<str:cpf>/editar/', reserva.update, name='update'),
    #path('<str:cpf>/excluir/', reserva.delete, name='delete'),
    #path('buscar/', reserva.search, name='search'),
]