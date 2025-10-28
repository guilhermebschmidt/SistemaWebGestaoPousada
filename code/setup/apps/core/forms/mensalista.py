from django import forms
from ..models.mensalista import Mensalista 
from ..models.hospede import Hospede

class MensalistaForm(forms.ModelForm): 
    hospede = forms.ModelChoiceField(
        queryset=Hospede.objects.filter(mensalista__isnull=True), 
        label="Hóspede",
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'})
    )

    class Meta:
        model = Mensalista
        fields = [
            'hospede', 
            'quarto', 
            'valor_mensal', 
            'dia_vencimento', 
            'data_inicio',
            'ativo',
            'observacoes'
        ]
        widgets = {
            'quarto': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'valor_mensal': forms.NumberInput(attrs={'class': 'input input-bordered w-full'}),
            'dia_vencimento': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'min': 1, 'max': 31}),
            'data_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'input input-bordered w-full', 'type': 'date'}
            ),
            'ativo': forms.CheckboxInput(attrs={'class': 'checkbox'}),
            'observacoes': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
        }