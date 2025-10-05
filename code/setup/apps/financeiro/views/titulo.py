from django.shortcuts import render, redirect, get_object_or_404
from ..models.titulo import Titulo
from ..forms.titulo import TituloForm
import datetime
from django.utils import timezone

def list_titulos(request):
    filtro_pago = request.GET.get('pago', 'todos')
    filtro_tipo = request.GET.get('tipo', 'todos')

    queryset = Titulo.objects.select_related('hospede', 'reserva').all().order_by('data_vencimento')

    if filtro_pago == 'sim':
        queryset = queryset.filter(pago=True)
    elif filtro_pago == 'nao':
        queryset = queryset.filter(pago=False)

    if filtro_tipo == 'entrada':
        queryset = queryset.filter(tipo=True)
    elif filtro_tipo == 'saida':
        queryset = queryset.filter(tipo=False)

    context = {
        'titulos': queryset,
        'filtro_pago': filtro_pago,
        'filtro_tipo': filtro_tipo,
        'hoje': datetime.date.today(),
    }
    return render(request, 'financeiro/titulo/listar.html', context)

def form(request, pk=None):
    instance = None
    if pk:
        instance = get_object_or_404(Titulo, pk=pk)

    if request.method == 'POST':
        form = TituloForm(request.POST, instance=instance)
        if form.is_valid():
            titulo = form.save(commit=False)
            titulo.save()

            return redirect('financeiro:list')
    else:
        form = TituloForm(instance=instance)

    context = {
        'form': form
    }

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