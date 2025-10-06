from django import forms
from ..models.quarto import Quarto

class QuartoForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['numero','capacidade' , 'descricao', 'preco']
        widgets = {
            'numero': forms.TextInput(attrs={
                'class': 'input input-bordered w-full'
            }),
           'capacidade': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'step': '1'
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
class QuartoStatusForm(forms.ModelForm):
    class Meta:
        model = Quarto
        fields = ['status'] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].widget.attrs.update({'class': 'select select-bordered w-full'})