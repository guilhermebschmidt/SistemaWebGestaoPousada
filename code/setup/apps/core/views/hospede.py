from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from ..models import Hospede, Reserva
from django.contrib import messages
from ..forms import HospedeForm
from django.contrib import messages

def listar(request):
    hospedes = Hospede.objects.all()
    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

def hospede_form(request, pk=None): 
    if pk:
        hospede = get_object_or_404(Hospede, pk=pk)
        success_message = "Hóspede atualizado com sucesso!"
    else:
        hospede = None
        success_message = "Hóspede cadastrado com sucesso!"

    if request.method == 'POST':
        
        form = HospedeForm(request.POST, instance=hospede)

        if form.is_valid(): 
            form.save() 
            messages.success(request, success_message)
            return redirect('hospede:listar') 
    
    else: 
        form = HospedeForm(instance=hospede)

    context = {
        'form': form,
        'hospede': hospede 
    }
    return render(request, 'core/hospede/form.html', context)

def excluir(request, pk):
    hospede = get_object_or_404(Hospede, pk=pk)
    reservas_ativas = hospede.reserva_set.exclude(status='Cancelada')
    
    if reservas_ativas.exists():
        messages.error(request, 'Este hóspede não pode ser excluído pois possui reservas ativas.')
        
        return redirect('/hospedes/')

    if request.method == 'POST':
        hospede.delete()
        messages.success(request, 'Hóspede excluído com sucesso.')
        return redirect('/hospedes/')
    return render(request, 'core/hospede/hospede_confirm_delete.html', {'hospede': hospede})

def buscar(request):
    nome = request.GET.get('search', '')
    if nome:
        hospedes = Hospede.objects.filter(nome__icontains=nome)
    else:
        hospedes = Hospede.objects.all()

    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

def detalhes(request, pk):
    hospede = get_object_or_404(Hospede, pk=pk)
    return render(request, 'core/hospede/detalhes.html', {'hospede': hospede})

def historico_hospede(request, pk):
    hospede = get_object_or_404(Hospede, pk=pk)
    reservas = Reserva.objects.filter(id_hospede=hospede).order_by('-data_reserva_inicio')
    return render(request, 'core/hospede/historico.html', {
        'hospede': hospede,
        'reservas': reservas
    })
