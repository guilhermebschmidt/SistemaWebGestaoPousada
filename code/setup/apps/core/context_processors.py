from apps.core.models import Notificacao

def notificacoes(request):
    if not request.user.is_authenticated:
        return {'notificacoes_topo': [], 'qtd_nao_lidas': 0}

    notificacoes_qs = Notificacao.objects.filter(usuario=request.user).order_by('-criado_em')[:10]
    
    qtd_nao_lidas = Notificacao.objects.filter(usuario=request.user, lida=False).count()

    notificacoes_formatadas = []
    for n in notificacoes_qs:
        icone = 'fas fa-info-circle'
        cor = 'text-gray-500'
        bg = 'bg-gray-100'
        
        if n.tipo == 'reserva':
            icone = 'fas fa-calendar-check'
            cor = 'text-primary'
            bg = 'bg-primary/10'
        elif n.tipo == 'hospede':
            icone = 'fas fa-user-plus'
            cor = 'text-success'
            bg = 'bg-success/10'
        elif n.tipo == 'financeiro':
            icone = 'fas fa-dollar-sign'
            cor = 'text-warning'
            bg = 'bg-warning/10'
            
        notificacoes_formatadas.append({
            'obj': n,
            'icone': icone,
            'cor': cor,
            'bg': bg
        })

    return {
        'notificacoes_topo': notificacoes_formatadas,
        'qtd_nao_lidas': qtd_nao_lidas
    }