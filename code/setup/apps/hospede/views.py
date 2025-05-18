from django.shortcuts import render
from .models import Hospede



def hospede(request):
    hospedes = Hospede.objects.all()
    return render(request, 'hospede/hospedes.html', {'hospede': hospedes})

def hospede_create(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        nome = request.POST.get('nome')
        telefone = request.POST.get('telefone')
        email = request.POST.get('email')
        data_nascimento = request.POST.get('data_nascimento')

        hospede = Hospede(
            cpf=cpf,
            nome=nome,
            telefone=telefone,
            email=email,
            data_nascimento=data_nascimento
        )
        hospede.save()
        return render(request, 'hospede/hospedes.html', {'hospede': hospede})
    return render(request, 'hospede/hospedes.html')

def hospede_update(request, cpf):
    hospede = Hospede.objects.get(cpf=cpf)
    if request.method == 'POST':
        hospede.nome = request.POST.get('nome')
        hospede.telefone = request.POST.get('telefone')
        hospede.email = request.POST.get('email')
        hospede.data_nascimento = request.POST.get('data_nascimento')
        hospede.save()
        return render(request, 'hospede/hospedes.html', {'hospede': hospede})
    return render(request, 'hospede/hospedes.html', {'hospede': hospede})

def hospede_delete(request, cpf):
    hospede = Hospede.objects.get(cpf=cpf)
    if request.method == 'POST':
        hospede.delete()
        return render(request, 'hospede/hospedes.html')
    return render(request, 'hospede/hospedes.html', {'hospede': hospede})

def hospede_search(request):
    if request.method == 'POST':
        search = request.POST.get('search')
        hospede = Hospede.objects.filter(nome__icontains=search)
        return render(request, 'hospede/hospedes.html', {'hospede': hospede})
    return render(request, 'hospede/hospedes.html')

def hospede_detail(request, cpf):
    hospede = Hospede.objects.get(cpf=cpf)
    return render(request, 'hospede/hospedes.html', {'hospede': hospede})

def hospede_list(request):
    hospede = Hospede.objects.all()
    return render(request, 'hospede/hospedes.html', {'hospede': hospede})

