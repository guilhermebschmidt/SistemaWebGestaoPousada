from django.urls import path
from ..views.relatorio_faturamento import relatorio_faturamento

urlpatterns = [
    path('faturamento/', relatorio_faturamento, name='relatorio_faturamento'),
]
