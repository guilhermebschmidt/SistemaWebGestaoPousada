from django.shortcuts import render
from django.db.models import Sum
from django.contrib import messages
from apps.financeiro.models import Titulo
from apps.core.models import Reserva
from apps.relatorios.calculos import ocupacao
import datetime

def painel_dashboard(request):
    hoje = datetime.date.today()
    data_inicio_default = hoje.replace(day=1)
    data_fim_default = hoje
    data_inicio_str = request.GET.get('data_inicio', data_inicio_default.strftime('%Y-%m-%d'))
    data_fim_str = request.GET.get('data_fim', data_fim_default.strftime('%Y-%m-%d'))

    try:
        data_inicio = datetime.datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        data_fim = datetime.datetime.strptime(data_fim_str, '%Y-%m-%d').date()
    except ValueError:
        data_inicio = data_inicio_default
        data_fim = data_fim_default
        messages.error(request, "Datas inválidas, usando o mês atual como padrão.")

    titulos_pagos = Titulo.objects.filter(
        cancelado=False,
        pago=True,
        data_pagamento__range=[data_inicio, data_fim]
    )

    receitas_agregado = titulos_pagos.filter(tipo=True).aggregate(total=Sum('valor'))
    receitas = receitas_agregado['total'] or 0
    despesas_agregado = titulos_pagos.filter(tipo=False).aggregate(total=Sum('valor'))
    despesas = despesas_agregado['total'] or 0
    balanco = receitas - despesas

    hospedes_ativos_count = Reserva.objects.filter(status='ATIVA').count()
    
    try:
        dados_ocupacao = ocupacao.gerar_relatorio_de_ocupacao(data_inicio, data_fim)
        if 'erro' in dados_ocupacao:
            taxa_ocupacao = 0.0
            messages.warning(request, f"Cálculo de Ocupação: {dados_ocupacao['erro']}")
        else:
            taxa_ocupacao = dados_ocupacao.get('taxa_ocupacao', 0.00)
    except Exception as e:
        messages.warning(request, f"Não foi possível calcular a taxa de ocupação: {e}")
        taxa_ocupacao = 0.0

    context = {
        'data_inicio': data_inicio.strftime('%Y-%m-%d'),
        'data_fim': data_fim.strftime('%Y-%m-%d'),
        'receitas': receitas,
        'despesas': despesas,
        'balanco': balanco,
        'hospedes_ativos_count': hospedes_ativos_count,
        'taxa_ocupacao': taxa_ocupacao,
    }
    
    return render(request, 'index.html', context)