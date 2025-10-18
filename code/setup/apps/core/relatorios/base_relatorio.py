from ..models import Reserva
'''
Arquivo para adicionar cálculos reutilizáveis que são utilizados tanto nos relatórios de
ocupação quanto nos relatórios financeiros.
'''

def get_receita_bruta_por_periodo(data_inicio, data_fim):
    """
    Busca e calcula a receita bruta total de reservas em um período.
    """
    reservas = Reserva.objects.filter(
        data_reserva_inicio__lt=data_fim,
        data_reserva_fim__gt=data_inicio
    ).exclude(status='CANCELADA')
    
    total_receita = sum(reserva.valor for reserva in reservas)
    return total_receita


