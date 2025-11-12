from django import forms
from ..models import Categoria

class CategoriaDespesaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Ex: Alimentação, Transporte...'}),
        }
        labels={
            'descricao': 'descricao',
        }
        help_texts = {
            'descricao': 'Insira uma categoria de despesa',
        }
        error_messages = {
            'descricao': {'required': 'Este campo é obrigatório.'},        
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)