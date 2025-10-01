from django.urls import path
import apps.financeiro.views.titulo as views


app_name = 'financeiro'

urlpatterns = [
    path('', views.list_titulos, name='list'),
    path('novo/', views.form, name='form'),
    path('editar/<int:pk>/', views.form, name='update'),
    path('titulos/<int:pk>/marcar-pago/', views.marcar_pago, name='marcar_pago'),
]
