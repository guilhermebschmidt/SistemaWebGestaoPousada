from django import forms
from .models import Quarto

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'status', 'descricao', 'preco']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'toggle toggle-primary'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': '0.01'
            }),
        }