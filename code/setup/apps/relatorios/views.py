from apps.core.models import Reserva, Quarto
from .calculos import ocupacao
from django.shortcuts import render
from datetime import date 
from dateutil.relativedelta import relativedelta
from .utils import exportar_relatorio_csv, exportar_relatorio_pdf
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
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
    data_fim_str = request.GET.get('data_fim', (
        today.replace(day=1) + relativedelta(months=1, days=-1)).strftime('%Y-%m-%d'))

    data_inicio = date.fromisoformat(data_inicio_str)
    data_fim = date.fromisoformat(data_fim_str)

    try:
        data_inicio = date.fromisoformat(data_inicio_str)
        data_fim = date.fromisoformat(data_fim_str)

        if data_inicio > data_fim:
            raise ValueError("Data de início após data de fim.")
        
    except ValueError:
        data_inicio = today.replace(day=1)
        data_fim = today.replace(day=1) + relativedelta(months=1, days=-1)
        raise ValueError (request, "Formato de data inválido no filtro.")

    # ------ 
    export_format = request.GET.get('export')
    dados_relatorio = ocupacao.gerar_relatorio_de_ocupacao(data_inicio, data_fim)
    
    # ------ Lógica de Exportação CSV --------- #
    if export_format == 'csv' and not dados_relatorio.get('erro'):

        cabecalhos_csv = ['Indicador', 'Valor']

        dados_csv = [
                ('Período Início', data_inicio.strftime('%d/%m/%Y')),
                ('Período Fim', data_fim.strftime('%d/%m/%Y')),
                ('Quantidade de Dias no Período', dados_relatorio['num_dias_periodo']),
                ('Nº de Novas Reservas no Período', dados_relatorio['numero_de_estadias_iniciadas']),
                ('Nº de Quartos Distintos Ocupados', dados_relatorio['quartos_distintos_ocupados']),
                ('Quantidade de Hóspedes no Período', dados_relatorio['quantidade_hospedes']),
                ('Dias-Quarto Disponíveis', dados_relatorio['dias_disponiveis']),
                ('Dias-Quarto Ocupados', dados_relatorio['dias_ocupados']),
                ('Taxa de Ocupação (%)', f"{dados_relatorio['taxa_ocupacao']:.2f}"),
                ('Duração Média das Estadias (dias)', f"{dados_relatorio['duracao_media']:.0f}"),
                ('Quarto Mais Popular', dados_relatorio['quarto_mais_ocupado']),
                ('Quarto Menos Popular', dados_relatorio['quarto_menos_ocupado']),
                ('Tipo de Quarto Mais Popular', dados_relatorio['tipo_quarto_mais_ocupado']),
                ('Tipo de Quarto Menos Popular', dados_relatorio['tipo_quarto_menos_ocupado']),
            ]
        
    
        return exportar_relatorio_csv(
            nome_arquivo_base='relatorio_ocupacao', 
            cabecalhos=cabecalhos_csv, 
            dados_linhas=dados_csv,
            request=request 
        )

    # ------ Lógica de Exportação PDF --------- #
    elif export_format == 'pdf' and not dados_relatorio.get('erro'):

        titulo_pdf = 'Relatório de Ocupação'
        periodo_str = f"Período Analisado: {
            data_inicio.strftime('%d/%m/%Y')} a{
                data_fim.strftime(' %d/%m/%Y')} ({
                    dados_relatorio.get('num_dias_periodo', 0)
                } dias)"
        
        styles = getSampleStyleSheet()

        dados_pdf = [

            [Paragraph('<b>Indicador</b>', styles['Normal']),
              Paragraph('<b>Valor</b>', styles['Normal'])
              ],
            
            ['Nº de Novas Reservas no Período', dados_relatorio.get('numero_de_estadias_iniciadas')],             ['Dias-Quarto Disponíveis', dados_relatorio.get('dias_disponiveis')],
            ['Dias-Quarto Ocupados', dados_relatorio.get('dias_ocupados')],
            ['Taxa de Ocupação (%)', f"{dados_relatorio['taxa_ocupacao']:.2f}"],
            ['Nº de Quartos Distintos Ocupados', dados_relatorio.get('quartos_distintos_ocupados')],
            ['Quantidade de Hóspedes no Período', dados_relatorio.get('quantidade_hospedes')],  
            ['Duração Média da Estadia (dias)', f"{dados_relatorio['duracao_media']:.0f}"],
            ['Quarto Mais Popular', dados_relatorio.get('quarto_mais_ocupado')],
            ['Quarto Menos Popular', dados_relatorio.get('quarto_menos_ocupado')],
            ['Tipo de Quarto Mais Popular', dados_relatorio.get('tipo_quarto_mais_ocupado')],
            ['Tipo de Quarto Menos Popular', dados_relatorio.get('tipo_quarto_menos_ocupado')],
        ]

        return exportar_relatorio_pdf(
            nome_arquivo_base='relatorio_ocupacao', 
            titulo_pdf=titulo_pdf,
            periodo_str=periodo_str,
            dados_tabela=dados_pdf, 
            request=request
        )
    
    context = {
        'data_inicio': data_inicio,
        'data_fim':data_fim,
        'dados': dados_relatorio,
       
    }
    
    return render(request, 'relatorios/ocupacao.html', context)

