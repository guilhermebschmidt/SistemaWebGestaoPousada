from django.urls import path
from .. import views

urlpatterns = [
    path('', views.list_titulos, name='list'),
    path('novo/', views.form, name='form'),
    path('editar/<int:pk>/', views.form, name='update'),
    path('titulos/<int:pk>/marcar-pago/', views.marcar_pago, name='marcar_pago'),
]