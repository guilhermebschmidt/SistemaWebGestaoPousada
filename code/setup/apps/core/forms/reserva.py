from django import forms
from ..models.reserva import Reserva
from ..models.hospede import Hospede
from ..models.quarto import Quarto
import datetime

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['id_hospede', 'id_quarto', 'data_check_in', 'data_check_out', 'valor']
        widgets = {
            'hospede': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'quarto': forms.Select(attrs={'class': 'select select-bordered w-full'}),
            'data_check_in': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'data_check_out': forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}),
            'valor': forms.NumberInput(attrs={'class': 'input input-bordered w-full', 'step': '0.01'}),
        }
        labels = {
            'hospede': 'Hóspede',
            'quarto': 'Quarto',
            'data_check_in': 'Data de Entrada',
            'data_check_out': 'Data de Saída',
            'valor': 'Valor da Reserva',
        }
        help_texts = {
            'id_hospede': 'Selecione o hóspede para a reserva.',
            'id_quarto': 'Selecione o quarto reservado.',
            'data_check_in': 'Informe a data de entrada.',
            'data_check_out': 'Informe a data de saída.',
            'valor': 'Informe o valor total da reserva.',
        }
        error_messages = {
            'id_hospede': {
                'required': 'Este campo é obrigatório.',
            },
            'id_quarto': {
                'required': 'Este campo é obrigatório.',
            },
            'data_check_in': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe uma data válida.',
            },
            'data_check_out': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe uma data válida.',
            },
            'valor': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe um valor numérico válido.',
            },
        }

    def clean_data_check_in(self):
        data_check_in = self.cleaned_data.get('data_check_in')
        if data_check_in and data_check_in < datetime.date.today():
            raise forms.ValidationError("A data de entrada não pode ser no passado.")
        return data_check_in

    def clean_data_check_out(self):
        data_check_out = self.cleaned_data.get('data_check_out')
        data_check_in = self.cleaned_data.get('data_check_in')

        if data_check_out and data_check_in:
            if data_check_out <= data_check_in:
                raise forms.ValidationError("A data de saída deve ser depois da data de entrada.")
        return data_check_out

    def clean_valor(self):
        valor = self.cleaned_data.get('valor')
        if valor is not None and valor <= 0:
            raise forms.ValidationError("O valor deve ser maior que zero.")
        return valor

    def __str__(self):
        return f"Reserva #{self.instance.pk} - Hóspede {self.instance.id_hospede} - Quarto {self.instance.id_quarto}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Carregar hóspedes ativos ou todos (filtrar se quiser)
        self.fields['id_hospede'].queryset = Hospede.objects.all().order_by('nome')
        # Carregar quartos disponíveis ou todos (filtrar se quiser)
        self.fields['id_quarto'].queryset = Quarto.objects.all().order_by('numero')  # exemplo se tiver campo numero
