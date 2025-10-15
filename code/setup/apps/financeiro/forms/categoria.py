from django import forms
from ..models import Categoria

class CategoriaDespesaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['descricao']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Alimentação, Transporte...'}),
        }