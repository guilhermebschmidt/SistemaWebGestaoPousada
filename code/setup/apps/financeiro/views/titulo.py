from django.shortcuts import render, redirect, get_object_or_404
from ..models.titulo import Titulo
from ..forms.titulo import TituloForm
from django.utils import timezone
from datetime import datetime

def list_titulos(request):
    queryset = Titulo.objects.select_related('hospede', 'reserva', 'categoria').all().order_by('data_vencimento')

    # Captura dos filtros
    filtro_pago = request.GET.get('pago')
    filtro_tipo_doc = request.GET.get('tipo_documento')
    filtro_tipo = request.GET.get('tipo')  # Entrada / Saída
    filtro_cancelado = request.GET.get('cancelado')
    filtro_hospede = request.GET.get('hospede')
    filtro_data_inicio = request.GET.get('data_inicio')
    filtro_data_fim = request.GET.get('data_fim')

    # 🔹 Filtro por pagamento
    if filtro_pago == 'sim':
        queryset = queryset.filter(pago=True)
    elif filtro_pago == 'nao':
        queryset = queryset.filter(pago=False)

    # 🔹 Filtro por tipo de documento
    if filtro_tipo_doc:
        queryset = queryset.filter(tipo_documento=filtro_tipo_doc)

    # 🔹 Filtro por tipo (Entrada / Saída)
    if filtro_tipo:
        if filtro_tipo.lower() == 'entrada':
            queryset = queryset.filter(tipo=True)
        elif filtro_tipo.lower() == 'saida':
            queryset = queryset.filter(tipo=False)

    # 🔹 Filtro por cancelado
    if filtro_cancelado == 'sim':
        queryset = queryset.filter(cancelado=True)
    elif filtro_cancelado == 'nao':
        queryset = queryset.filter(cancelado=False)

    # 🔹 Filtro por hóspede (busca parcial)
    if filtro_hospede:
        queryset = queryset.filter(hospede__nome__icontains=filtro_hospede.strip())

    # 🔹 Filtro por data de vencimento — agora com conversão segura
    formato_data = "%Y-%m-%d"
    if filtro_data_inicio:
        try:
            data_inicio = datetime.strptime(filtro_data_inicio, formato_data).date()
            queryset = queryset.filter(data_vencimento__gte=data_inicio)
        except ValueError:
            pass  # ignora formato inválido

    if filtro_data_fim:
        try:
            data_fim = datetime.strptime(filtro_data_fim, formato_data).date()
            queryset = queryset.filter(data_vencimento__lte=data_fim)
        except ValueError:
            pass

    context = {
        'titulos': queryset,
        'filtros': {
            'pago': filtro_pago,
            'tipo_documento': filtro_tipo_doc,
            'tipo': filtro_tipo,
            'cancelado': filtro_cancelado,
            'hospede': filtro_hospede,
            'data_inicio': filtro_data_inicio,
            'data_fim': filtro_data_fim,
        },
        'hoje': timezone.now().date(),
    }

    return render(request, 'financeiro/titulo/listar.html', context)

def titulo_form(request, pk=None):
    if pk:
        titulo = get_object_or_404(Titulo, pk=pk)
    else:
        titulo = None

    if request.method == 'POST':
        form = TituloForm(request.POST, instance=titulo)
        if form.is_valid():
            form.save()
            return redirect('financeiro:list_titulos')
    else:
        form = TituloForm(instance=titulo)

    context = {
        'form': form,
        'titulo': titulo,
    }
    return render(request, 'financeiro/titulo/form.html', context)

def marcar_pago(request, pk):
    titulo = get_object_or_404(Titulo, pk=pk)
    titulo.pago = True
    titulo.data_pagamento = timezone.now().date()
    titulo.save()
    return redirect('financeiro:list_titulos')