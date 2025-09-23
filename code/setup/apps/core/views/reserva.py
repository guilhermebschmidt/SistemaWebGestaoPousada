from django.shortcuts import render, redirect, get_object_or_404
from ..models.reserva import Reserva
from ..models.hospede import Hospede
from ..forms.reserva  import ReservaForm
import datetime
from django.utils import timezone
from django.http import JsonResponse

def list(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

def list_checkin(request):
    hoje = datetime.date.today()
    reservas = Reserva.objects.filter(data_reserva_inicio = hoje)
    return render(request, 'core/reserva/list_check_in.html', {'reservas': reservas})

def list_checkout(request):
    hoje = datetime.date.today()
    reservas = Reserva.objects.filter(data_reserva_fim = hoje)
    return render(request, 'core/reserva/list_check_out.html', {'reservas': reservas})

def add(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            return redirect('reserva:list')
    else:
        form = ReservaForm()

    return render(request, 'core/reserva/form.html', {'form': form})


def update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            return redirect('reserva:list')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'core/reserva/form.html', {'form': form, 'reserva': reserva})


def cancelar_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method != 'POST':
        return render(request, 'core/reserva/confirmar_cancelamento.html', {'reserva': reserva})
    motivo = request.POST.get('motivo_cancelamento', 'Motivo não especificado.')
    reserva.status = 'CANCELADA'
    reserva.motivo_cancelamento = motivo
    reserva.save()
    return redirect('reserva:list')

def search(request):
    query = request.GET.get('q', '')
    reservas = Reserva.objects.filter(id_hospede__nome__icontains=query)
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

def marcar_checkin(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.data_check_in = timezone.now()
    reserva.status = 'ATIVA'
    reserva.save()
    return redirect('reserva:list_checkin')

def marcar_checkout(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.data_check_out = timezone.now()
    reserva.status = 'CONCLUIDA'
    reserva.save()
    return redirect('reserva:list_checkout')

def buscar_hospedes(request):
    if 'term' in request.GET:
        qs = Hospede.objects.filter(nome__icontains=request.GET.get('term'))
        hospedes = []
        for hospede in qs:
            hospedes.append({
                'id': hospede.cpf,
                'label': hospede.nome,
                'value': hospede.nome
            })
        return JsonResponse(hospedes, safe=False)
    return JsonResponse([], safe=False)
