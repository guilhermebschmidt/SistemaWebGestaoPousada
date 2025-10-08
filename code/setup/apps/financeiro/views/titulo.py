from django.shortcuts import render, redirect, get_object_or_404
from ..models.titulo import Titulo
from ..forms.titulo import TituloForm
import datetime
from django.utils import timezone

def list_titulos(request):
    queryset = Titulo.objects.select_related('hospede', 'reserva').all().order_by('data_vencimento')

    filtro_pago = request.GET.get('pago')
    filtro_tipo_doc = request.GET.get('tipo_documento')
    filtro_tipo = request.GET.get('tipo')  # Entrada / Saída
    filtro_cancelado = request.GET.get('cancelado')
    filtro_hospede = request.GET.get('hospede')
    filtro_data_inicio = request.GET.get('data_inicio')
    filtro_data_fim = request.GET.get('data_fim')

    if filtro_pago == 'sim':
        queryset = queryset.filter(pago=True)
    elif filtro_pago == 'nao':
        queryset = queryset.filter(pago=False)

    if filtro_tipo_doc:
        queryset = queryset.filter(tipo_documento=filtro_tipo_doc)

    if filtro_tipo:
        if filtro_tipo.lower() == 'entrada':
            queryset = queryset.filter(tipo=True)
        elif filtro_tipo.lower() == 'saida':
            queryset = queryset.filter(tipo=False)

    if filtro_cancelado == 'sim':
        queryset = queryset.filter(cancelado=True)
    elif filtro_cancelado == 'nao':
        queryset = queryset.filter(cancelado=False)

    if filtro_hospede:
        queryset = queryset.filter(hospede__nome__icontains=filtro_hospede)

    if filtro_data_inicio:
        queryset = queryset.filter(data_vencimento__gte=filtro_data_inicio)
    if filtro_data_fim:
        queryset = queryset.filter(data_vencimento__lte=filtro_data_fim)

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
        'hoje': datetime.date.today(),
    }

    return render(request, 'financeiro/titulo/listar.html', context)


def form(request, pk=None):
    instance = get_object_or_404(Titulo, pk=pk) if pk else None

    if request.method == 'POST':
        form = TituloForm(request.POST, instance=instance)
        if form.is_valid():
            titulo = form.save(commit=False)
            titulo.save()
            # se o form tiver campos M2M:
            form.save_m2m()
            return redirect('financeiro:list')
        else:
            print(form.errors)  # 👈 ajuda a depurar
    else:
        form = TituloForm(instance=instance)

    context = {'form': form}
    return render(request, 'financeiro/titulo/form.html', context)


def marcar_pago(request, pk):
    titulo = get_object_or_404(Titulo, pk=pk)

    titulo.pago = True
    titulo.data_pagamento = timezone.now().date()
    titulo.save()

    # Confirma reserva vinculada
    if titulo.reserva:
        titulo.reserva.status = "CONFIRMADA"
        titulo.reserva.save()

    return redirect('financeiro:list')