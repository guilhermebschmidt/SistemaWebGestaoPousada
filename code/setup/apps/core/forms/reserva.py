from django import forms
from ..models.reserva import Reserva
from ..models.hospede import Hospede
from ..models.quarto import Quarto
import datetime

class ReservaForm(forms.ModelForm):
    hospede_nome = forms.CharField(
        label='Hóspede',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Digite para buscar um hóspede...'
        }),
        help_text='Selecione o hóspede para a reserva.'
    )
    class Meta:
        model = Reserva
        fields = ['id_hospede', 'id_quarto', 'data_reserva_inicio', 'data_reserva_fim']
        widgets = {
            'id_quarto': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'data_reserva_inicio': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'input input-bordered w-full',
                    'type': 'date'
                }
            ),
            'data_reserva_fim': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'input input-bordered w-full',
                    'type': 'date'
                }
            ),
        }
        labels = {
            'id_hospede': 'Hóspede',
            'id_quarto': 'Quarto',
            'data_reserva_inicio': 'Data início da Reserva',
            'data_reserva_fim': 'Data fim da Reserva',
        }
        help_texts = {
            'id_hospede': 'Selecione o hóspede para a reserva.',
            'id_quarto': 'Selecione o quarto reservado.',
            'data_reserva_inicio': 'Informe a data de início da reserva.',
            'data_reserva_fim': 'Informe a data de fim da reserva.',
        }
        error_messages = {
            'id_hospede': {
                'required': 'Este campo é obrigatório.',
            },
            'id_quarto': {
                'required': 'Este campo é obrigatório.',
            },
            'data_reserva_inicio': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe uma data válida.',
            },
            'data_reserva_fim': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe uma data válida.',
            },
        }

    def clean_data_reserva_inicio(self):
        data_inicio = self.cleaned_data.get('data_reserva_inicio')
        if data_inicio and data_inicio < datetime.date.today():
            raise forms.ValidationError("A data de início não pode ser anterior à data atual.")
        return data_inicio

    def clean_data_reserva_fim(self):
        data_fim = self.cleaned_data.get('data_reserva_fim')
        data_inicio = self.cleaned_data.get('data_reserva_inicio')

        if data_fim and data_inicio:
            if data_fim <= data_inicio:
                raise forms.ValidationError("A data de fim deve ser posterior à data de início.")
        return data_fim

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_hospede'].widget = forms.HiddenInput()
        if self.instance and self.instance.pk:
            self.fields['hospede_nome'].initial = self.instance.id_hospede.nome
        self.fields['id_quarto'].queryset = Quarto.objects.all().order_by('numero')
