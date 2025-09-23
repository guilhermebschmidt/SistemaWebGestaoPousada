from django.shortcuts import render, redirect, get_object_or_404
from ..models.titulo import Titulo
from ..forms.titulo import TituloForm
import datetime

def list_titulos(request):
    filtro_pago = request.GET.get('pago', 'aberto')

    queryset = Titulo.objects.select_related('hospede', 'reserva').all().order_by('data_vencimento')

    if filtro_pago == 'sim':
        queryset = queryset.filter(pago=True)
    elif filtro_pago == 'nao':
        queryset = queryset.filter(pago=False)

    context = {
        'titulos': queryset,
        'filtro_pago': filtro_pago,
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
            form.save()
            return redirect('financeiro:list')
    else:
        form = TituloForm(instance=instance)

    context = {
        'form': form
    }

    return render(request, 'financeiro/titulo/form.html', context)