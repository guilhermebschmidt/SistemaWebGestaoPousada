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
        print("📥 Dados recebidos no POST:")
        print(request.POST)

        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save()
            return redirect('reserva:list')
        else:
            print("⚠️ Erros de validação:")
            print(form.errors)
    else:
        form = ReservaForm()

    return render(request, 'core/reserva/form.html', {'form': form})


def update(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    if request.method == 'POST':
        form = ReservaForm(request.POST, instance=reserva)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.data_check_in = form.cleaned_data['data_reserva']
            reserva.save()
            return redirect('reserva:list')
    else:
        form = ReservaForm(instance=reserva)

    return render(request, 'core/reserva/form.html', {'form': form, 'reserva': reserva})

def delete(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)
    if request.method == 'POST':
        reserva.delete()
        return redirect('reserva:list')
    # Caso queira, renderize uma confirmação antes:
    return render(request, 'core/reserva/confirm_delete.html', {'reserva': reserva})

def search(request):
    query = request.GET.get('q', '')
    reservas = Reserva.objects.filter(id_hospede__nome__icontains=query)
    return render(request, 'core/reserva/list.html', {'reservas': reservas})