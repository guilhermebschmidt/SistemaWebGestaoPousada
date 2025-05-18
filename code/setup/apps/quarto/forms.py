from django import forms
from .models import Quarto  

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'status']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'numero': 'Número do Quarto',
            'status': 'Status',
            'descricao': 'Descrição',
        }
        help_texts = {
            'numero': 'Insira o número do quarto.',
            'status': 'Selecione se o quarto está disponível.',
            'descricao': 'Insira uma descrição do quarto.',
        }
        error_messages = {
            'numero': {
                'required': 'Este campo é obrigatório.',
                'max_length': 'O número do quarto deve ter no máximo 100 caracteres.',
            },
            'status': {
                'required': 'Este campo é obrigatório.',
            },
            'descricao': {
                'max_length': 'A descrição deve ter no máximo 100 caracteres.',
            },
        }