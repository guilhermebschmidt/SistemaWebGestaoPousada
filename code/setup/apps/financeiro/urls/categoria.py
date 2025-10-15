from django.urls import path
from .. import views 

urlpatterns = [
    path('categorias/', views.CategoriaDespesaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', views.CategoriaDespesaCreateView.as_view(), name='categoria_create'),
]