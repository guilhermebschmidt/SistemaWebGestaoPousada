from django.shortcuts import render, get_object_or_404, redirect
from ..models import Hospede
from django.contrib.auth.decorators import login_required

@login_required
def hospede_list(request):
    hospedes = Hospede.objects.all()
    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

@login_required
def hospede_create(request):
    if request.method == 'POST':
        Hospede.objects.create(
            cpf=request.POST.get('cpf'),
            nome=request.POST.get('nome'),
            telefone=request.POST.get('telefone'),
            email=request.POST.get('email'),
            data_nascimento=request.POST.get('data_nascimento')
        )
        return redirect('/hospedes/')
    return render(request, 'core/hospede/form.html')

@login_required
def hospede_update(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    if request.method == 'POST':
        hospede.nome = request.POST.get('nome')
        hospede.telefone = request.POST.get('telefone')
        hospede.email = request.POST.get('email')
        hospede.data_nascimento = request.POST.get('data_nascimento')
        hospede.save()
        return redirect('/hospedes/')
    return render(request, 'core/hospede/form.html', {'hospede': hospede})

@login_required
def hospede_delete(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    if request.method == 'POST':
        hospede.delete()
        return redirect('/hospedes/')
    return render(request, 'core/hospede/hospede_confirm_delete.html', {'hospede': hospede})

@login_required
def hospede_search(request):
    hospedes = []
    if request.method == 'POST':
        search = request.POST.get('search')
        hospedes = Hospede.objects.filter(nome__icontains=search)
    return render(request, 'core/hospede/listar.html', {'hospedes': hospedes})

@login_required
def hospede_detail(request, cpf):
    hospede = get_object_or_404(Hospede, cpf=cpf)
    return render(request, 'core/hospede/hospede_detail.html', {'hospede': hospede})
