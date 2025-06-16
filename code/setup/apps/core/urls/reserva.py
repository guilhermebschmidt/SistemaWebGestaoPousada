from django.urls import path
import apps.core.views.reserva as reserva

urlpatterns = [
    path('', reserva.list, name='list'),
    path('novo/', reserva.add, name='form'),
    path('<str:cpf>/', reserva.details, name='details'),
    path('<str:cpf>/editar/', reserva.update, name='update'),
    path('<str:cpf>/excluir/', reserva.delete, name='delete'),
    path('buscar/', reserva.search, name='search'),
]