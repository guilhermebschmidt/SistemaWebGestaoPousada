from django import forms
from ..models import Hospede
import datetime


class HospedeForm(forms.ModelForm):
    model = Hospede
    fields = ['nome', 'cpf', 'data_nascimento', 'telefone', 'email']
    widgets = {
        'nome': forms.TextInput(attrs={'class': 'form-control'}),
        'cpf': forms.TextInput(attrs={'class': 'form-control'}),
        'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        'email': forms.EmailInput(attrs={'class': 'form-control'}),
    }
    labels = {
        'nome': 'Nome do Hóspede',
        'cpf': 'CPF',
        'data_nascimento': 'Data de Nascimento',
        'telefone': 'Telefone',
        'email': 'Email',
    }
    help_texts = {
        'nome': 'Insira o nome do hóspede.',
        'cpf': 'Insira o CPF do hóspede.',
        'data_nascimento': 'Insira a data de nascimento do hóspede.',
        'telefone': 'Insira o telefone do hóspede.',
        'email': 'Insira o email do hóspede.',
    }
    error_messages = {
        'nome': {
            'required': 'Este campo é obrigatório.',
            'max_length': 'O nome deve ter no máximo 100 caracteres.',
        },
        'cpf': {
            'required': 'Este campo é obrigatório.',
            'max_length': 'O CPF deve ter no máximo 100 caracteres.',
        },
        'data_nascimento': {
            'required': 'Este campo é obrigatório.',
        },
        'telefone': {
            'required': 'Este campo é obrigatório.',
            'max_length': 'O telefone deve ter no máximo 100 caracteres.',
        },
        'email': {
            'required': 'Este campo é obrigatório.',
            'max_length': 'O email deve ter no máximo 100 caracteres.',
        },
    }

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf.isdigit():
            raise forms.ValidationError("O CPF deve conter apenas números.")
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone.isdigit():
            raise forms.ValidationError("O telefone deve conter apenas números.")
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if '@' not in email or '.' not in email:
            raise forms.ValidationError("Insira um email válido.")
        return email

    def clean_data_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_nascimento')
        if data_nascimento > datetime.date.today():
            raise forms.ValidationError("A data de nascimento não pode ser futura.")
        return data_nascimento