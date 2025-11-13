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

        if not data_inicio:
            return data_inicio

        if data_inicio < data_minima_reserva:
            raise forms.ValidationError(
                f"A data de início da reserva deve ser a partir de {data_minima_reserva.strftime('%d/%m/%Y')}."
            )
        return data_inicio

    # Tornar quantidade de adultos/crianças opcionais no form (os defaults do model já cuidam)
    quantidade_adultos = forms.IntegerField(required=False, initial=1)
    quantidade_criancas = forms.IntegerField(required=False, initial=0)

    def clean(self):
        cleaned_data = super().clean()     
        
        data_inicio = cleaned_data.get('data_reserva_inicio')
        data_fim = cleaned_data.get('data_reserva_fim')
        quarto = cleaned_data.get('id_quarto')
        id_hospede = cleaned_data.get('id_hospede')

        # Converte os valores da chave estrangeira (IDs) em instâncias do modelo quando necessário
        if id_hospede and not isinstance(id_hospede, Hospede):
            try:
                hospede_obj = Hospede.objects.get(pk=id_hospede)
                cleaned_data['id_hospede'] = hospede_obj
            except Exception:
                pass

        if quarto and not isinstance(quarto, Quarto):
            try:
                quarto_obj = Quarto.objects.get(pk=quarto)
                quarto = quarto_obj
                cleaned_data['id_quarto'] = quarto_obj
            except Exception:
                pass
        # Usar defaults do form/model quando os campos vierem ausentes no POST
        adultos = cleaned_data.get('quantidade_adultos')
        if adultos is None:
            adultos = getattr(self.fields['quantidade_adultos'], 'initial', 1) or 1
        criancas = cleaned_data.get('quantidade_criancas')
        if criancas is None:
            criancas = getattr(self.fields['quantidade_criancas'], 'initial', 0) or 0

        # Prepare uma lista para mensagens não-field e evite adicionar mensagens duplicadas
        non_field_msgs = []

        # Se um quarto foi submetido mas não aparece em cleaned_data, é provável que o
        # campo tenha sido validado como "invalid choice" porque o queryset foi filtrado
        # (por exemplo: quarto indisponível para as datas). Detectamos esse caso e
        # tentamos construir uma mensagem detalhada com o período conflitante.
        submitted_quarto = None
        try:
            submitted_quarto = self.data.get('id_quarto') if getattr(self, 'data', None) else None
        except Exception:
            submitted_quarto = None
        if submitted_quarto and not quarto:
            try:
                if Quarto.objects.filter(pk=submitted_quarto).exists():
                    # tentar recuperar um conflito específico para mostrar as datas
                    try:
                        quarto_obj = Quarto.objects.get(pk=submitted_quarto)
                        conflito = verifica_conflito_de_datas(quarto_obj, data_inicio, data_fim, reserva_a_ignorar=self.instance)
                        if conflito:
                            non_field_msgs.append(
                                f"ERRO: O quarto selecionado já está reservado no período de "
                                f"{conflito.data_reserva_inicio.strftime('%d/%m/%Y')} a "
                                f"{conflito.data_reserva_fim.strftime('%d/%m/%Y')}."
                            )
                        else:
                            non_field_msgs.append('ERRO: O quarto selecionado já está reservado')
                    except Exception:
                        non_field_msgs.append('ERRO: O quarto selecionado já está reservado')
            except Exception:
                pass

        if data_inicio == None:
            raise forms.ValidationError(
                f"Selecione uma data para início da reserva!"
            )
        
        if data_fim == None:
            raise forms.ValidationError(
                f"Selecione uma data para o fim da reserva!"
            )
        
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
                # Mensagem detalhada com período conflitante (apenas uma ocorrência)
                non_field_msgs.append(
                    f"ERRO: O quarto selecionado já está reservado no período de "
                    f"{reserva_conflitante.data_reserva_inicio.strftime('%d/%m/%Y')} a "
                    f"{reserva_conflitante.data_reserva_fim.strftime('%d/%m/%Y')}."
                )
                
        # Adicionar mensagens não-field únicas ao form (preserva ordem de inserção)
        if non_field_msgs:
            seen = set()
            unique_msgs = []
            for m in non_field_msgs:
                if m not in seen:
                    seen.add(m)
                    unique_msgs.append(m)
            for m in unique_msgs:
                self.add_error(None, m)

        return cleaned_data
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_hospede'].widget = forms.HiddenInput()
        
        if self.instance and self.instance.pk:
            self.fields['hospede_nome'].initial = self.instance.id_hospede.nome
        # Por padrão considera apenas quartos com status 'DISPONIVEL'
        quartos_qs = Quarto.objects.filter(status='DISPONIVEL').order_by('numero')

        # Tentar obter datas informadas para filtrar apenas quartos disponíveis
        data_inicio = None
        data_fim = None

        # valores podem vir em self.data (quando POST) ou em initial/instance
        data = getattr(self, 'data', None)
        if data:
            try:
                data_inicio = data.get('data_reserva_inicio')
                data_fim = data.get('data_reserva_fim')
            except Exception:
                data_inicio = data_fim = None

        # se não vierem via POST, verificar initial/instance
        if not data_inicio or not data_fim:
            if self.initial:
                data_inicio = data_inicio or self.initial.get('data_reserva_inicio')
                data_fim = data_fim or self.initial.get('data_reserva_fim')
            if self.instance and self.instance.pk:
                data_inicio = data_inicio or self.instance.data_reserva_inicio
                data_fim = data_fim or self.instance.data_reserva_fim

        # Se tivermos ambas as datas, excluir quartos com reservas conflitantes
        if data_inicio and data_fim:
            try:
                # garantir objetos datetime.date
                if isinstance(data_inicio, str):
                    from datetime import datetime
                    data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                if isinstance(data_fim, str):
                    from datetime import datetime
                    data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

                from ..models.reserva import Reserva
                STATUS_BLOQUEANTES = ['CONFIRMADA', 'ATIVA', 'CONCLUIDA']
                conflitos = Reserva.objects.filter(
                    data_reserva_inicio__lt=data_fim,
                    data_reserva_fim__gt=data_inicio,
                    status__in=STATUS_BLOQUEANTES,
                )
                if self.instance and self.instance.pk:
                    conflitos = conflitos.exclude(pk=self.instance.pk)

                quartos_indisponiveis = conflitos.values_list('id_quarto_id', flat=True)
                quartos_qs = quartos_qs.exclude(pk__in=list(quartos_indisponiveis))
            except Exception:
                # em caso de erro ao parsear datas, manter lista completa de quartos disponíveis
                pass

        self.fields['id_quarto'].queryset = quartos_qs
