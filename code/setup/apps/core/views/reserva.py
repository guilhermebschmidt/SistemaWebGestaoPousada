from django.shortcuts import render, redirect, get_object_or_404
from ..models.reserva import Reserva
from ..forms.reserva  import ReservaForm
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def list(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

@login_required
def list_checkin(request):
    hoje = datetime.date.today()
    reservas = Reserva.objects.filter(data_reserva_inicio = hoje)
    return render(request, 'core/reserva/list_check_in.html', {'reservas': reservas})

@login_required
def list_checkout(request):
    hoje = datetime.date.today()
    reservas = Reserva.objects.filter(data_reserva_fim = hoje)
    return render(request, 'core/reserva/list_check_out.html', {'reservas': reservas})

@login_required
def add(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            return redirect('reserva:list')
    else:
        form = ReservaForm()

    return render(request, 'core/reserva/form.html', {'form': form})

@login_required
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

@login_required
def delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reserva:list')
    return render(request, 'core/reserva/confirm_delete.html', {'reserva': reserva})

@login_required
def search(request):
    query = request.GET.get('q', '')
    reservas = Reserva.objects.filter(id_hospede__nome__icontains=query)
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

@login_required
def marcar_checkin(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.data_check_in = timezone.now()
    reserva.save()
    return redirect('reserva:list_checkin')

@login_required
def marcar_checkout(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    reserva.data_check_out = timezone.now()
    reserva.save()
    return redirect('reserva:list_checkout')