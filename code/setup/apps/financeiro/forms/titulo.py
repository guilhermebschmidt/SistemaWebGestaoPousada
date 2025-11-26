from django import forms
from ..models.titulo import Titulo

class TituloForm(forms.ModelForm):
    BOOLEAN_CHOICES = [
        (True, 'Sim'),
        (False, 'Não')
    ]
    TIPO_CHOICES = [
        (True, 'Entrada'),
        (False, 'Saída')
    ]

    tipo = forms.TypedChoiceField(
        label="Tipo do Título",
        choices=TIPO_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        initial=True
    )
    pago = forms.TypedChoiceField(
        label="Pago?",
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        initial=False,
        required=False,
    )
    cancelado = forms.TypedChoiceField(
        label="Cancelado?",
        choices=BOOLEAN_CHOICES,
        widget=forms.RadioSelect,
        coerce=lambda x: x == 'True',
        initial=False
    )

    class Meta:
        model = Titulo
        fields = [
            'descricao', 'valor', 'tipo_documento', 'conta_corrente',
            'data', 'data_vencimento', 'data_pagamento', 'data_compensacao',
            'hospede', 'reserva', 'tipo', 'cancelado', 'pago', 'observacao',
            'categoria' 
        ]

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'valor': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'step': '0.01'}),
            'tipo_documento': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'conta_corrente': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'data': forms.DateInput(
                attrs={'class': 'input input-bordered w-full', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_vencimento': forms.DateInput(
                attrs={'class': 'input input-bordered w-full', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_pagamento': forms.DateInput(
                attrs={'class': 'input input-bordered w-full', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'data_compensacao': forms.DateInput(
                attrs={'class': 'input input-bordered w-full', 'type': 'date'},
                format='%Y-%m-%d'
            ),
            'hospede': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'reserva': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'observacao': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'select select-bordered w-full'}), 
        }
        labels = {
            'data': 'Data de Emissão',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hospede'].required = False
        self.fields['reserva'].required = False
        self.fields['categoria'].required = False

    def clean(self):
        cleaned_data = super().clean()
        
        tipo = cleaned_data.get('tipo')
        categoria = cleaned_data.get('categoria')

        if categoria and tipo is True:
            self.add_error('tipo', "Não é permitido lançar 'Entrada' vinculada a uma Categoria de despesa.")
            self.add_error('categoria', "Se você selecionou uma Categoria, o tipo deve ser 'Saída'.")

        return cleaned_data