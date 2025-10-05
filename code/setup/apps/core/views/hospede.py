from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ValidationError
from ..models import Hospede, Reserva

def listar(request):
    hospedes = Hospede.objects.all()
    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

def form(request, cpf=None):
    hospede = get_object_or_404(Hospede, cpf=cpf) if cpf else None
    errors = None

    if request.method == 'POST':
        if hospede:
            hospede.nome = request.POST.get('nome')
            hospede.telefone = request.POST.get('telefone')
            hospede.email = request.POST.get('email')
            hospede.data_nascimento = request.POST.get('data_nascimento')
            hospede.rua = request.POST.get('rua')
            hospede.numero = request.POST.get('numero')
            hospede.complemento = request.POST.get('complemento')
            hospede.bairro = request.POST.get('bairro')
            hospede.cidade = request.POST.get('cidade')
            hospede.cep = request.POST.get('cep')
        else:
            hospede = Hospede(
                cpf=request.POST.get('cpf'),
                nome=request.POST.get('nome'),
                telefone=request.POST.get('telefone'),
                email=request.POST.get('email'),
                data_nascimento=request.POST.get('data_nascimento'),
                rua=request.POST.get('rua'),
                numero=request.POST.get('numero'),
                complemento=request.POST.get('complemento'),
                bairro=request.POST.get('bairro'),
                cidade=request.POST.get('cidade'),
                cep=request.POST.get('cep'),
            )

        try:
            hospede.clean()  
            hospede.save()
            return redirect('/hospedes/')
        except ValidationError as e:
            errors = [str(err) for err in e.error_list]

    return render(request, 'core/hospede/form.html', {
        'hospede': hospede,
        'errors': errors
    })

def excluir(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    if request.method == 'POST':
        hospede.delete()
        return redirect('/hospedes/')
    return render(request, 'core/hospede/hospede_confirm_delete.html', {'hospede': hospede})

def buscar(request):
    nome = request.GET.get('search', '')
    if nome:
        hospedes = Hospede.objects.filter(nome__icontains=nome)
    else:
        hospedes = Hospede.objects.all()

    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

def detalhes(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    return render(request, 'core/hospede/detalhes.html', {'hospede': hospede})

def historico_hospede(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    reservas = Reserva.objects.filter(id_hospede=hospede).order_by('-data_reserva_inicio')
    return render(request, 'core/hospede/historico.html', {
        'hospede': hospede,
        'reservas': reservas
    })
