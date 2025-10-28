from django.urls import path
from apps.core.views import mensalista 

app_name = 'mensalista'

urlpatterns = [
    path('', mensalista.MensalistaListView.as_view(), name='listar_mensalistas'),
    path('adicionar/', mensalista.MensalistaCreateView.as_view(), name='adicionar_mensalista'),
]