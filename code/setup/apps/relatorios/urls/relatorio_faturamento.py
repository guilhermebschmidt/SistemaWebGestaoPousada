from django.urls import path
from ..views.relatorio_faturamento import relatorio_faturamento

urlpatterns = [
    path('relatorio/faturamento/', relatorio_faturamento, name='relatorio_faturamento'),
    
]
