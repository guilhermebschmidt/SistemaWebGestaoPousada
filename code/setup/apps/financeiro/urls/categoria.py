from django.urls import path
from ..views.categoria import CategoriaDespesaListView, CategoriaDespesaCreateView

urlpatterns = [
    path('categorias/', CategoriaDespesaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', CategoriaDespesaCreateView.as_view(), name='categoria_create'),
]

"""
from django.urls import path
from .. import views 

urlpatterns = [
    path('categorias/', views.CategoriaDespesaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', views.CategoriaDespesaCreateView.as_view(), name='categoria_create'),
]
"""