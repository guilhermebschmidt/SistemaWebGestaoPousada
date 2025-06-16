from django.shortcuts import render, redirect, get_object_or_404
from ..models.reserva import Reserva
from ..forms.reserva  import ReservaForm

# Create your views here.
def list(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

def list_checkin(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/reserva/list.html', {'reservas': reservas})

def add(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            # Define data_checkin igual à data_reserva
            reserva.data_checkin = form.cleaned_data['data_reserva']
            reserva.save()
            return redirect('reserva:list')
    else:
        form = ReservaForm()

    return render(request, 'core/reserva/form.html', {'form': form})

def update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.data_checkin = form.cleaned_data['data_reserva']
            reserva.save()
            return redirect('reserva:list')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'core/reserva/form.html', {'form': form, 'reserva': reserva})