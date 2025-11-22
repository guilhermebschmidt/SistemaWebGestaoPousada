from django.utils import timezone
from apps.core.models import Reserva, Hospede
import datetime

def notificacoes(request):
    hoje = datetime.date.today()
    
    notificacoes_list = []
    
    checkins_hoje = Reserva.objects.filter(
        data_reserva_inicio=hoje, 
        status__in=['CONFIRMADA', 'PREVISTA']
    ).count()
    
    if checkins_hoje > 0:
        notificacoes_list.append({
            'tipo': 'checkin',
            'icone': 'fas fa-key',
            'cor_bg': 'bg-warning/10',
            'cor_texto': 'text-warning',
            'titulo': f'Você tem {checkins_hoje} Check-ins hoje',
            'tempo': 'Hoje'
        })

    ultimas_reservas = Reserva.objects.order_by('-id')[:3]
    
    for reserva in ultimas_reservas:
        notificacoes_list.append({
            'tipo': 'reserva',
            'icone': 'fas fa-calendar-check',
            'cor_bg': 'bg-primary/10',
            'cor_texto': 'text-primary',
            'titulo': f'Reserva #{reserva.id} - {reserva.id_hospede.nome}',
            'tempo': 'Recente'
        })

    ultimos_hospedes = Hospede.objects.order_by('-id')[:2]
    for hospede in ultimos_hospedes:
        notificacoes_list.append({
            'tipo': 'hospede',
            'icone': 'fas fa-user-plus',
            'cor_bg': 'bg-success/10',
            'cor_texto': 'text-success',
            'titulo': f'Novo hóspede: {hospede.nome}',
            'tempo': 'Recente'
        })

    return {
        'lista_notificacoes': notificacoes_list,
        'total_notificacoes': len(notificacoes_list)
    }