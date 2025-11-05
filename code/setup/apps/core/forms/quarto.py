from django import forms
from ..models.quarto import Quarto

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero','capacidade' , 'tipo_quarto', 'descricao', 'preco']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Insira o Número do quarto'
            }),
           'capacidade': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': '1',
                'placeholder':''

            }),
            'tipo_quarto':forms.Select(attrs={
                'class': 'select select-bordered w-full',
                'placeholder': 'Selecione o tipo do quarto'
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'textarea textarea-bordered w-full',
                'rows': 3,
                'placeholder':'Insira uma descrição para o quarto'
            }),
            'preco': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': '0.01',
                'placeholder': 'Insira o preço do quarto'
            }),
        }
        labels ={
            'numero':'Número do Quarto',
            'capacidade':'Capacidade' , 
            'tipo_quarto':'Tipo', 
            'descricao':'Descrição',
            'preco':'Preço',
        }
        help_texts = {
            'numero': 'Insira o número do quarto',
            'capacidade': 'Insira a capacidade máxima do quarto',
            'tipo_quarto': 'Insira o tipo do quarto',
            'descricao': 'Insira uma descrição para o quarto',
            'preco': '0.00',
        }
        error_messages = {
            'numero': {'required': 'Este campo é obrigatório.'},
            'capacidade': {'required': 'Este campo é obrigatório.'},
            'tipo_quarto': {'required': 'Este campo é obrigatório.'},
            'preco': {'required': 'Este campo é obrigatório.'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar descricao obrigatório no formulário para corresponder aos testes
        # que esperam erro quando está vazio.
        if 'descricao' in self.fields:
            self.fields['descricao'].required = True


class QuartoStatusForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['status'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'select select-bordered w-full'})
