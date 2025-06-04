from django import forms
from .models import Quarto

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero', 'status', 'descricao', 'preco']  # adicionado descricao e preco
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'numero': 'Número do Quarto',
            'status': 'Disponível?',
            'descricao': 'Descrição',
            'preco': 'Preço por noite',
        }
        help_texts = {
            'numero': 'Insira o número do quarto.',
            'status': 'Marque se o quarto está disponível.',
            'descricao': 'Insira uma descrição do quarto.',
            'preco': 'Informe o valor da diária.',
        }
