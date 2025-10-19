from apps.core.models import Reserva, Quarto
from .calculos import ocupacao
from django.shortcuts import render
from datetime import date 
from dateutil import relativedelta

'''
View para funções dos relatórios de ocupação e financeiros.
'''

def relatorio_ocupacao(request):
    '''
    View 
    '''
    today = date.today()
    data_inicio_str = request.GET.get('data_inicio', today.replace(day=1).strftime('%Y-%m-%d'))
    data_fim_str = request.GET.get('data_fim', (today.replace(day=1) + relativedelta(months=1, days=-1)).strftime('%Y-%m-%d'))

    data_inicio = date.fromisoformat(data_inicio_str)
    data_fim = date.fromisoformat(data_fim_str)

    dados_relatorio = ocupacao.gerar_relatorio_de_ocupacao(data_inicio, data_fim)
    
    context = {
        'data_inicio': data_inicio,
        'data_fim':data_fim,
        'dados': dados_relatorio,
       
    }
    return render(request, 'relatorios/ocupacao.html', context)