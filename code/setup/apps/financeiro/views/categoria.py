from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from ..models import Categoria
from ..forms import CategoriaDespesaForm

class CategoriaDespesaListView(ListView):
    model = Categoria
    template_name = 'financeiro/categoria/listar.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.filter(tipo='D')

class CategoriaDespesaCreateView(CreateView):
    model = Categoria
    form_class = CategoriaDespesaForm
    template_name = 'financeiro/categoria/form.html' 
    success_url = reverse_lazy('financeiro:categoria_list')

    def form_valid(self, form):
        form.instance.tipo = 'D'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = 'Nova Categoria de Despesa'
        return context