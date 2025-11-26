from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from ..models.mensalista import Mensalista 
from ..forms.mensalista import MensalistaForm 

class MensalistaListView(ListView):
    model = Mensalista 
    template_name = 'core/mensalista/mensalista_list.html'  
    context_object_name = 'mensalistas' 

    def get_queryset(self):
        return Mensalista.objects.order_by('-ativo', 'hospede__nome') 

class MensalistaCreateView(CreateView):
    model = Mensalista 
    form_class = MensalistaForm 
    template_name = 'core/mensalista/mensalista_form.html' 
    success_url = reverse_lazy('mensalista:listar_mensalistas') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Adicionar Mensalista"
        return context
    
class MensalistaUpdateView(UpdateView):
    model = Mensalista
    form_class = MensalistaForm
    template_name = 'core/mensalista/mensalista_form.html'
    success_url = reverse_lazy('mensalista:listar_mensalistas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar Mensalista"
        return context