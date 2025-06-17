from django.shortcuts import render, redirect, get_object_or_404
from ..models.reserva import Reserva

# Create your views here.
def list(request):
    reservas = Reserva.objects.all()
    return render(request, 'core/reserva/listar.html', {'reservas': reservas})

def add(request):
    if request.method == 'POST':
        Reserva.objects.create(
            cpf=request.POST.get('cpf'),
            nome=request.POST.get('nome'),
            telefone=request.POST.get('telefone'),
            email=request.POST.get('email'),
            data_nascimento=request.POST.get('data_nascimento')
        )
        return redirect('/reservas/')
    return render(request, 'core/reserva/form.html')

def update(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    if request.method == 'POST':
        hospede.nome = request.POST.get('nome')
        hospede.telefone = request.POST.get('telefone')
        hospede.email = request.POST.get('email')
        hospede.data_nascimento = request.POST.get('data_nascimento')
        hospede.save()
        return redirect('/reservas/')
    return render(request, 'core/reserva/form.html', {'hospede': hospede})

def delete(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    if request.method == 'POST':
        hospede.delete()
        return redirect('/hospedes/')
    return render(request, 'core/hospede/hospede_confirm_delete.html', {'hospede': hospede})

def search(request):
    hospedes = []
    if request.method == 'POST':
        search = request.POST.get('search')
        hospedes = Hospede.objects.filter(nome__icontains=search)
    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

def details(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    return render(request, 'core/hospede/hospede_detail.html', {'hospede': hospede})
