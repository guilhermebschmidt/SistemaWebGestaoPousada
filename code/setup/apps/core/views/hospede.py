from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from ..models import Hospede, Reserva
from ..forms import HospedeForm

def listar(request):
    hospedes = Hospede.objects.all().order_by('-id')
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
    
    if request.method == 'POST':
        reservas_pendentes = Reserva.objects.filter(
            id_hospede=hospede,
            status__in=['PREVISTA', 'CONFIRMADA', 'ATIVA']
        ).exists()

        if reservas_pendentes:
            messages.error(request, f"Não é possível excluir {hospede.nome}. Existem reservas Ativas ou Futuras vinculadas a este hóspede.")
            return redirect('hospede:listar')

        try:
            nome_hospede = hospede.nome
            hospede.delete()
            messages.success(request, f"Hóspede {nome_hospede} excluído com sucesso.")
        except Exception as e:
            messages.error(request, f"Erro ao excluir hóspede: {e}")
            
        return redirect('hospede:listar')
        
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