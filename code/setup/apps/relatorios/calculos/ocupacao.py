from apps.core.models import Quarto, Reserva
from apps.financeiro.models import Titulo
from datetime import date
from django.db.models import Sum, F

'''
Arquivo para adicionar cálculos utilizados nos relatórios de ocupação.
'''
def _calcular_dias_ocupados_no_periodo(data_inicio_relatorio, data_fim_relatorio, reservas_validas):
    """
    Função auxiliar interna que calcula o total de dias-quarto ocupado em um determinado período.
    Dias-quarto = quantidade de quarto x numero de dias do periodo
    """
    total_dias_ocupados = 0

    for reserva in reservas_validas:
        
        inicio_sobreposicao = max(reserva.data_reserva_inicio, data_inicio_relatorio)
        fim_sobreposicao = min(reserva.data_reserva_fim, data_fim_relatorio)
        
        dias_no_periodo = (fim_sobreposicao - inicio_sobreposicao).days
        
        if dias_no_periodo > 0:
            total_dias_ocupados += dias_no_periodo
            
    return total_dias_ocupados

def gerar_relatorio_de_ocupacao(data_inicio, data_fim):
    """
    Calcula e retorna um dicionário com os principais KPIs de ocupação para um período.
    """
    if not isinstance(data_inicio, date) or not isinstance(data_fim, date):
        raise TypeError("Adicione uma data de início e um data de fim para o relatório")

    if data_inicio > data_fim:
        return {
            'erro': 'A data de início não pode ser posterior à data de fim.'
        }
    
    '''
    Cálculo da quantidade de reservas dentro do período selecionado 
     (exclui reservas previstas e reservas canceladas)
    '''
    STATUS_DE_OCUPACAO = ['CONFIRMADA', 'ATIVA', 'CONCLUÍDA']

    reservas_validas = Reserva.objects.filter(
        data_reserva_inicio__lt=data_fim,
        data_reserva_fim__gt=data_inicio,
        status__in=STATUS_DE_OCUPACAO 
    )   

    '''
    Cálculo taxa de ocupação por período: 
    Taxa de Ocupação= (Total de Dias-Quarto Ocupados/Total de Dias-Quarto Disponíveis)* 100
    '''
    dias_quarto_ocupados = _calcular_dias_ocupados_no_periodo(data_inicio, data_fim, reservas_validas)
    
    num_dias_periodo = (data_fim - data_inicio).days + 1
    total_quartos = Quarto.objects.count()
    dias_quarto_disponiveis = total_quartos * num_dias_periodo
    
    taxa_ocupacao = 0
    if dias_quarto_disponiveis > 0:
        taxa_ocupacao= (dias_quarto_ocupados/dias_quarto_disponiveis)*100

    '''
    Cálculo de quartos distintos ocupados no período
    '''
    quartos_distintos_ocupados = reservas_validas.values('id_quarto').distinct().count()   

    '''
    Cálculo da quantidade dos hóspedes presentes na pousada (soma quantidade de pessoas em cada reserva)
    '''
    resultado_hospedes = reservas_validas.aggregate(
        total_hospedes=Sum(F('quantidade_adultos') + F('quantidade_criancas'))
    )
    quantidade_hospedes = resultado_hospedes['total_hospedes'] or 0

    '''
    Cálculo da Duração Média das Reservas:
    Soma total dos dias de todas as reservas/Número total de reservas
    '''
    reservas_iniciadas_no_periodo = Reserva.objects.filter(
        data_reserva_inicio__range=(data_inicio, data_fim),
        status__in=STATUS_DE_OCUPACAO 
    )

    numero_de_reservas = reservas_iniciadas_no_periodo.count()

    soma_das_duracoes = reservas_iniciadas_no_periodo.aggregate(
        duracao_total=Sum(F('data_reserva_fim') - F('data_reserva_inicio'))
    )['duracao_total']

    duracao_media = 0
    if numero_de_reservas > 0 and soma_das_duracoes is not None:
        duracao_media = soma_das_duracoes.days / numero_de_reservas

    return {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_quartos_pousada': total_quartos,
        'dias_disponiveis': dias_quarto_disponiveis,
        'dias_ocupados': dias_quarto_ocupados,
        'taxa_ocupacao': taxa_ocupacao,
        'quartos_distintos_ocupados': quartos_distintos_ocupados, 
        'quantidade_hospedes': quantidade_hospedes, 
        'numero_de_estadias_iniciadas': numero_de_reservas,
        'duracao_media': duracao_media,                                                
    }


