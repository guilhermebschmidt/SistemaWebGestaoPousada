from apps.core.models import Reserva, Quarto
from .calculos import ocupacao
from django.shortcuts import render
from datetime import date 
from dateutil.relativedelta import relativedelta
from .utils import exportar_relatorio_csv

'''
View para funções dos relatórios de ocupação e financeiros.
'''

def relatorio_ocupacao(request):
    '''
    View que define o filtro por período e chama os dados que compõem o relátorio de ocupação  
    (calculados pela função gerar_relatorio_de_ocupação de calculos/ocupacao.py)
    '''
    today = date.today()
    data_inicio_str = request.GET.get('data_inicio', today.replace(day=1).strftime('%Y-%m-%d'))
    data_fim_str = request.GET.get('data_fim', (today.replace(day=1) + relativedelta(months=1, days=-1)).strftime('%Y-%m-%d'))

    data_inicio = date.fromisoformat(data_inicio_str)
    data_fim = date.fromisoformat(data_fim_str)

    dados_relatorio = ocupacao.gerar_relatorio_de_ocupacao(data_inicio, data_fim)
    
    # ------ Lógica de Exportação CSV --------- #
    if request.GET.get('export') == 'csv' and not dados_relatorio.get('erro'):

        cabecalhos_csv = ['Metrica', 'Valor']

        dados_csv = [
                ('Período Início', data_inicio.strftime('%d/%m/%Y')),
                ('Período Fim', data_fim.strftime('%d/%m/%Y')),
                ('Dias no Período', dados_relatorio['num_dias_periodo']),
                ('Número de Reservas', dados_relatorio['numero_de_estadias_iniciadas']),
                ('Quartos Distintos Ocupados', dados_relatorio['quartos_distintos_ocupados']),
                ('Total de Hóspedes', dados_relatorio['quantidade_hospedes']),
                ('Dias-Quarto Disponíveis', dados_relatorio['dias_disponiveis']),
                ('Dias-Quarto Ocupados', dados_relatorio['dias_ocupados']),
                ('Taxa de Ocupação (%)', f"{dados_relatorio['taxa_ocupacao']:.2f}"),
                ('Duração Média (dias)', f"{dados_relatorio['duracao_media']:.1f}"),
                ('Quarto Mais Ocupado', dados_relatorio['quarto_mais_ocupado']),
                ('Quarto Menos Ocupado', dados_relatorio['quarto_menos_ocupado']),
                ('Tipo Quarto Mais Popular', dados_relatorio['tipo_quarto_mais_ocupado']),
                ('Tipo de Quarto Menos Popular', dados_relatorio['tipo_quarto_menos_ocupado']),
            ]
        
    
        return exportar_relatorio_csv(
            nome_arquivo_base='relatorio_ocupacao', 
            cabecalhos=cabecalhos_csv, 
            dados_linhas=dados_csv,
            request=request 
        )

    context = {
        'data_inicio': data_inicio,
        'data_fim':data_fim,
        'dados': dados_relatorio,
       
    }
    return render(request, 'relatorios/ocupacao.html', context)

