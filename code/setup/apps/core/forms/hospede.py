from django import forms
from ..models import Hospede
import datetime
import re

class HospedeForm(forms.ModelForm):
    cpf = forms.CharField(
        label='CPF',
        max_length=14, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full', 
            'placeholder': '000.000.000-00' 
        }), 
        help_text='Insira o CPF do hóspede.'
    )
    class Meta:
        model = Hospede
        fields = [
            'nome', 'cpf', 'data_nascimento', 'telefone', 'email',
            'rua', 'numero', 'complemento', 'bairro', 'cidade', 'cep'
        ]
        
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Insira o nome completo do hóspede'
                }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'input input-bordered w-full', 
                'type': 'date' 
                }),
            'telefone': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '(00) 00000-0000'
                }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'exemplo@email.com'
                }),
            'rua': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Insira o nome da rua'
                }),
            'numero': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Número'
                }),
            'complemento': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Apto, Bloco, Casa (Opcional)'
                }),
            'bairro': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Insira o bairro'
                }),
            'cidade': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': 'Insira a cidade'
                }),
            'cep': forms.TextInput(attrs={
                'class': 'input input-bordered w-full',
                'placeholder': '0000-000'
                }),
        }
        labels = {
            'nome': 'Nome do Hóspede',
            'cpf': 'CPF',
            'data_nascimento': 'Data de Nascimento',
            'telefone': 'Telefone',
            'email': 'Email',
            'rua': 'Rua',
            'numero': 'Número',
            'complemento': 'Complemento',
            'bairro': 'Bairro',
            'cidade': 'Cidade',
            'cep': 'CEP',
        }
        help_texts = {
            'nome': 'Insira o nome do hóspede.',
            'cpf': 'Insira o CPF do hóspede.',
            'data_nascimento': 'Insira a data de nascimento do hóspede.',
            'telefone': 'Insira o telefone do hóspede.',
            'email': 'Insira o email do hóspede.',
            'rua': 'Insira o nome da rua.',
            'numero': 'Insira o número da residência.',
            'complemento': 'Complemento (opcional).',
            'bairro': 'Insira o bairro.',
            'cidade': 'Insira a cidade.',
            'cep': 'Insira o CEP.',
        }
        error_messages = {
            'nome': {'required': 'Este campo é obrigatório.'},
            'cpf': {'required': 'Este campo é obrigatório.'},
            'data_nascimento': {'required': 'Este campo é obrigatório.'},
            'telefone': {'required': 'Este campo é obrigatório.'},
            'email': {'required': 'Este campo é obrigatório.'},
            'rua': {'required': 'Este campo é obrigatório.'},
            'numero': {'required': 'Este campo é obrigatório.'},
            'bairro': {'required': 'Este campo é obrigatório.'},
            'cidade': {'required': 'Este campo é obrigatório.'},
            'cep': {'required': 'Este campo é obrigatório.'},
        }

    def clean_cpf(self):
        cpf_digitado = self.cleaned_data.get('cpf', '')

        if not cpf_digitado: # P/ adicionar passaporte
            return cpf_digitado 

        cpf_limpo = re.sub(r'\D', '', cpf_digitado)

        if not cpf_limpo.isdigit():
            raise forms.ValidationError("O CPF deve conter apenas números.")
        
        if len(cpf_limpo) != 11:
            raise forms.ValidationError("O CPF deve conter exatamente 11 dígitos.")
       
        query = Hospede.objects.filter(cpf=cpf_limpo) 

        if self.instance and self.instance.pk: 
            query = query.exclude(pk=self.instance.pk) 
    
        if query.exists(): 
            raise forms.ValidationError("Este CPF já está cadastrado para outro hóspede.")
            
        return cpf_limpo

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone', '').replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
        if not telefone.isdigit():
            raise forms.ValidationError("O telefone deve conter apenas números.")
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        if '@' not in email or '.' not in email:
            raise forms.ValidationError("Insira um email válido.")
        return email

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        hoje = datetime.date.today()

        if data_nascimento > hoje:
            raise forms.ValidationError("A data de nascimento não pode ser futura.")

        if data_nascimento.year >= hoje.year:
            raise forms.ValidationError("A data de nascimento não pode ser no ano atual ou em anos futuros.")

        idade = hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
        )

        if idade < 18:
            raise forms.ValidationError("O hóspede deve ter 18 anos ou mais.")

        return data_nascimento
