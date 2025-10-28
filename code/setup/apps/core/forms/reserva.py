from django import forms
from ..models.reserva import Reserva
from ..models.hospede import Hospede
from ..models.quarto import Quarto
from datetime import date, timedelta
from ..utils.conflito_datas import verifica_conflito_de_datas

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
        fields = ['id_hospede', 'id_quarto', 'data_reserva_inicio', 'data_reserva_fim', 'quantidade_adultos', 'quantidade_criancas']
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
            'quantidade_adultos': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': '1'
                }
            ),
            'quantidade_criancas': forms.NumberInput(attrs={
                'class': 'input input-bordered w-full',
                'min': '0'
                }
            ),
        }
        labels = {
            'id_hospede': 'Hóspede',
            'id_quarto': 'Quarto',
            'data_reserva_inicio': 'Data início da Reserva',
            'data_reserva_fim': 'Data fim da Reserva',
            'quantidade_adultos':'Quantidade de Adultos',
            'quantidade_criancas':'Quantidade de Crianças'
        }
        help_texts = {
            'id_hospede': 'Selecione o hóspede para a reserva.',
            'id_quarto': 'Selecione o quarto reservado.',
            'data_reserva_inicio': 'Informe a data de início da reserva.',
            'data_reserva_fim': 'Informe a data de fim da reserva.',
            'quantidade_adultos':'Quantidade de Adultos',
            'quantidade_criancas':'Quantidade de Crianças'
        }
        error_messages = {
            'id_hospede': {
                'required': 'Este campo é obrigatório.'
            },
            'id_quarto': {
                'required': 'Este campo é obrigatório.'
            },
            'data_reserva_inicio': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe uma data válida.',
            },
            'data_reserva_fim': {
                'required': 'Este campo é obrigatório.',
                'invalid': 'Informe uma data válida.',
            },
            'quantidade_adultos': {
                'required': 'Este campo é obrigatório.'
            },
            'quantidade_criancas': {
                'required': 'Este campo é obrigatório.'
            },
        }

    def clean_data_reserva_inicio(self):
        data_inicio = self.cleaned_data.get('data_reserva_inicio')

        '''
        Aplicação da regra de negócio - reserva com 2 dias de antecedência
        '''
        hoje = date.today()
        data_minima_reserva = hoje + timedelta(days=2)
       
        if data_inicio < data_minima_reserva:
            raise forms.ValidationError(
                f"A data de início da reserva deve ser a partir de {data_minima_reserva.strftime('%d/%m/%Y')}."
            )
        return data_inicio

    def clean(self):
        cleaned_data = super().clean()     
        
        data_inicio = cleaned_data.get('data_reserva_inicio')
        data_fim = cleaned_data.get('data_reserva_fim')
        quarto = cleaned_data.get('id_quarto')
        adultos = cleaned_data.get('quantidade_adultos') or 0
        criancas = cleaned_data.get('quantidade_criancas') or 0

        if data_fim and data_inicio:
            if data_fim <= data_inicio:
                self.add_error('data_reserva_fim', "A data de fim deve ser posterior à data de início.")

        if quarto:
            quantidade_pessoas = adultos + criancas
            if quantidade_pessoas < 1:
                self.add_error('quantidade_adultos', "A reserva deve ser para pelo menos 1 pessoa.")
            elif quantidade_pessoas > quarto.capacidade:
                self.add_error(None, 
                    f"A quantidade total de pessoas ({quantidade_pessoas}) excede a capacidade do quarto ({quarto.capacidade})."
                )
        if quarto and data_inicio and data_fim:
            reserva_conflitante = verifica_conflito_de_datas(quarto, data_inicio, data_fim, reserva_a_ignorar=self.instance)
            if reserva_conflitante:
                self.add_error(None, 
                    f'ERRO DE CONFLITO: Este quarto já está reservado no período de '
                    f'{reserva_conflitante.data_reserva_inicio.strftime("%d/%m/%Y")} a '
                    f'{reserva_conflitante.data_reserva_fim.strftime("%d/%m/%Y")}.'
                )
                
        return cleaned_data
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_hospede'].widget = forms.HiddenInput()
        
        if self.instance and self.instance.pk:
            self.fields['hospede_nome'].initial = self.instance.id_hospede.nome
        self.fields['id_quarto'].queryset = Quarto.objects.all().order_by('numero')
