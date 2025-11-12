from django.shortcuts import render
from django.db.models import Sum, Q
from ..models.titulo import Titulo 
import datetime

def balanco_financeiro(request):
    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str = request.GET.get('data_fim')

    hoje = datetime.date.today()
    data_inicio_default = hoje.replace(day=1)
    data_fim_default = hoje

    try:
        data_inicio = datetime.datetime.strptime(data_inicio_str, '%Y-%m-%d').date() if data_inicio_str else data_inicio_default
        data_fim = datetime.datetime.strptime(data_fim_str, '%Y-%m-%d').date() if data_fim_str else data_fim_default
    except ValueError:
        data_inicio = data_inicio_default
        data_fim = data_fim_default

    titulos_pagos_no_periodo = Titulo.objects.filter(
        tipo=True,                 
        cancelado=False,           
        pago=True,                 
        data_pagamento__isnull=False, 
        data_pagamento__range=[data_inicio, data_fim] 
    )

    resultado_soma = titulos_pagos_no_periodo.aggregate(
        total_arrecadado=Sum('valor')
    )

    total_arrecadado = resultado_soma['total_arrecadado'] or 0.00

    context = {
        'total_arrecadado': total_arrecadado,
        'titulos_list': titulos_pagos_no_periodo.order_by('-data_pagamento'),
        'data_inicio': data_inicio.strftime('%Y-%m-%d'),
        'data_fim': data_fim.strftime('%Y-%m-%d'),
    }

    return render(request, 'financeiro/balanco.html', context)