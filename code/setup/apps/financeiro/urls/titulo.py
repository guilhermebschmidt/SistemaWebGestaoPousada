from django.urls import path
from apps.financeiro.views.titulo import list_titulos, titulo_form, marcar_pago, cancelar_titulo

urlpatterns = [
    path('', list_titulos, name='list_titulos'),
    path('', list_titulos, name='list'),
    path('novo/', titulo_form, name='novo_titulo'),
    path('form/', titulo_form, name='form'),
    path('editar/<int:pk>/', titulo_form, name='editar_titulo'),
    path('<int:pk>/update/', titulo_form, name='update'),
    path('marcar_pago/<int:pk>/', marcar_pago, name='marcar_pago'),
    path('cancelar/<int:pk>/', cancelar_titulo, name='cancelar_titulo'),
]