from apps.core.models import Quarto, Reserva
from apps.financeiro.models import Titulo
from datetime import date
from django.db.models import Sum, F
from collections import defaultdict

'''
Arquivo com os cálculos dos dados que são utilizados nos relatórios de ocupação.
'''
def _calcular_dias_ocupados_no_periodo(data_inicio_relatorio, data_fim_relatorio, reservas_validas):
    """
    Função auxiliar interna que calcula o total de dias-quarto ocupado em um determinado período.
    Dias-quarto = quantidade de quartos x numero de dias do periodo
    """
    total_dias_ocupados = 0

    for reserva in reservas_validas:
        
        inicio_sobreposicao = max(reserva.data_reserva_inicio, data_inicio_relatorio)
        fim_sobreposicao = min(reserva.data_reserva_fim, data_fim_relatorio)
        
        dias_no_periodo = (fim_sobreposicao - inicio_sobreposicao).days
        
        if dias_no_periodo > 0:
            total_dias_ocupados += dias_no_periodo
            
    return total_dias_ocupados

def _calcular_dias_ocupados_por_quarto(data_inicio_relatorio, data_fim_relatorio, reservas_validas):
    """
    Calcula os dias-quarto ocupados para cada quarto no período
    """
    dias_por_quarto = defaultdict(int)
    
    for reserva in reservas_validas:
        inicio_sobreposicao = max(reserva.data_reserva_inicio, data_inicio_relatorio)
        fim_sobreposicao = min(reserva.data_reserva_fim, data_fim_relatorio)
        dias_no_periodo = (fim_sobreposicao - inicio_sobreposicao).days
        if dias_no_periodo > 0:
            dias_por_quarto[reserva.id_quarto_id] += dias_no_periodo 
            
    return dias_por_quarto


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
    ).select_related('id_quarto')   

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


    '''
    Cálculo dos quartos que tiveram mais e menos dias ocupados no período
    '''
    dias_ocupados_por_quarto = _calcular_dias_ocupados_por_quarto(data_inicio, data_fim, reservas_validas)
    dias_quarto_ocupados = sum(dias_ocupados_por_quarto.values())

    quarto_mais_ocupado_numero ="N/A"
    quarto_menos_ocupado_numero = "N/A"
    max_dias = -1
    min_dias = float('inf') 

    if dias_ocupados_por_quarto: 
        quarto_mais_ocupado_id = max(dias_ocupados_por_quarto, key=dias_ocupados_por_quarto.get)
        quarto_menos_ocupado_id = min(dias_ocupados_por_quarto, key=dias_ocupados_por_quarto.get)
        max_dias = dias_ocupados_por_quarto[quarto_mais_ocupado_id]
        min_dias = dias_ocupados_por_quarto[quarto_menos_ocupado_id]
        
        try:
             quarto_mais_ocupado_obj = Quarto.objects.get(id=quarto_mais_ocupado_id)
             quarto_menos_ocupado_obj = Quarto.objects.get(id=quarto_menos_ocupado_id)
             quarto_mais_ocupado_numero = str(quarto_mais_ocupado_obj)
             quarto_menos_ocupado_numero = str(quarto_menos_ocupado_obj)

        except Quarto.DoesNotExist:
             quarto_mais_ocupado_numero = "ID não encontrado"
             quarto_menos_ocupado_numero = "ID não encontrado"

    else: 
        quarto_mais_ocupado_numero = "N/A"
        quarto_menos_ocupado_numero = "N/A"
        max_dias = 0
        min_dias = 0

    '''
    Cálculo do tipo de quarto (tipo_quarto) mais ocupado e o menos ocupado
    '''
    quartos_distintos_ocupados = len(dias_ocupados_por_quarto)
    
    tipo_quarto_mais_ocupado_nome = "N/A"
    tipo_quarto_menos_ocupado_nome = "N/A"

    max_dias_por_tipo = 0
    min_dias_por_tipo = 0

    if dias_ocupados_por_quarto: 
        quartos_ocupados_ids = list(dias_ocupados_por_quarto.keys())
        quartos_info = Quarto.objects.filter(id__in=quartos_ocupados_ids).values('id', 'tipo_quarto')
        dict_quarto_tipo = {q['id']: q['tipo_quarto'] for q in quartos_info}
    
        dias_por_tipo = defaultdict(int)
        for quarto_id, dias in dias_ocupados_por_quarto.items():
            tipo = dict_quarto_tipo.get(quarto_id) 
            if tipo:
                dias_por_tipo[tipo] += dias

        if dias_por_tipo:
            tipo_quarto_mais_ocupado_key = max(dias_por_tipo, key=dias_por_tipo.get)
            tipo_quarto_menos_ocupado_key = min(dias_por_tipo, key=dias_por_tipo.get)
            max_dias_por_tipo = dias_por_tipo[tipo_quarto_mais_ocupado_key]    
            min_dias_por_tipo = dias_por_tipo[tipo_quarto_menos_ocupado_key]    
      
            tipo_quarto_mais_ocupado_nome = dict(Quarto.TIPOS_QUARTOS_CHOICES).get(
                tipo_quarto_mais_ocupado_key, tipo_quarto_mais_ocupado_key
            )
            tipo_quarto_menos_ocupado_nome = dict(Quarto.TIPOS_QUARTOS_CHOICES).get(
                tipo_quarto_menos_ocupado_key, tipo_quarto_menos_ocupado_key
            )

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
        'quarto_mais_ocupado':  quarto_mais_ocupado_numero,
        'quarto_menos_ocupado':  quarto_menos_ocupado_numero,
        'tipo_quarto_mais_ocupado': tipo_quarto_mais_ocupado_nome,        
        'tipo_quarto_menos_ocupado': tipo_quarto_menos_ocupado_nome,        

    }


