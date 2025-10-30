from django import forms
from ..models import Hospede
import datetime
import re

class HospedeForm(forms.ModelForm):

    cpf = forms.CharField(
        label='CPF',
        max_length=14, 
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full', 
            'placeholder': '000.000.000-00' 
        }), 
        help_text='Obrigatório se Passaporte não for preenchido'
    )
    passaporte = forms.CharField(
        label='Passaporte',
        max_length=15,
        required=False, 
        widget=forms.TextInput(attrs={
            'class': 'input input-bordered w-full',
            'placeholder': 'Número do Passaporte'
        }),
        help_text='Obrigatório se CPF não for preenchido.'
    )
    class Meta:
        model = Hospede
        fields = [
            'nome', 'cpf', 'passaporte','data_nascimento', 'telefone', 'email',
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
            'passaporte': 'Número do Passaporte',
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
            'nome': 'Insira o nome do hóspede',
            'data_nascimento': 'Insira a data de nascimento do hóspede',
            'telefone': 'Insira o telefone do hóspede',
            'email': 'Insira o email do hóspede',
            'rua': 'Insira o nome da rua',
            'numero': 'Insira o número da residência',
            'complemento': 'Complemento (opcional)',
            'bairro': 'Insira o bairro',
            'cidade': 'Insira a cidade',
            'cep': 'Insira o CEP',
        }
        error_messages = {
            'nome': {'required': 'Este campo é obrigatório.'},
            'data_nascimento': {'required': 'Este campo é obrigatório.'},
            'telefone': {'required': 'Este campo é obrigatório.'},
            'email': {'required': 'Este campo é obrigatório.'},
            'rua': {'required': 'Este campo é obrigatório.'},
            'numero': {'required': 'Este campo é obrigatório.'},
            'bairro': {'required': 'Este campo é obrigatório.'},
            'cidade': {'required': 'Este campo é obrigatório.'},
            'cep': {'required': 'Este campo é obrigatório.'},
        }

   
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
    
    def clean_cpf(self):
        cpf_digitado = self.cleaned_data.get('cpf', '')

        if not cpf_digitado: 
            return None 

        cpf_limpo = re.sub(r'\D', '', cpf_digitado)
        
        if not cpf_limpo.isdigit():
            raise forms.ValidationError("O CPF deve conter apenas números.")
        
        if len(cpf_limpo) != 11:
            raise forms.ValidationError("O CPF deve conter exatamente 11 dígitos.")
            
        return cpf_limpo

    def clean_passaporte(self):
        passaporte_digitado = self.cleaned_data.get('passaporte', '')

        if not passaporte_digitado:
            return None 
        
        passaporte_limpo = passaporte_digitado.strip().upper()
        
        return passaporte_limpo 


    """def clean (self):
        cleaned_data=super().clean()

        cpf=cleaned_data.get('cpf')
        passaporte=cleaned_data.get('passaporte')

        if not cpf and not passaporte:
            raise forms.ValidationError(
                'É obrigatório fornecer um CPF ou um número de Passaporte.'
            )

        if cpf and passaporte:
            raise forms.ValidationError(
                'Forneça apenas o CPF ou o Passaporte, não ambos.'
            )
        
        if cpf:
            query = Hospede.objects.filter(cpf=cpf) 
            if self.instance and self.instance.pk: 
                query = query.exclude(pk=self.instance.pk) 
            if query.exists(): 
                raise forms.ValidationError("Este CPF já está cadastrado para outro hóspede.")
        
        if passaporte:
            query = Hospede.objects.filter(passaporte=passaporte)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                raise forms.ValidationError("Este Passaporte já está cadastrado para outro hóspede.")
        
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)"""
    

    # Em apps/core/forms/hospede.py
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Pega os valores JÁ LIMPOS pelos métodos clean_cpf e clean_passaporte
        cpf = cleaned_data.get('cpf')
        passaporte = cleaned_data.get('passaporte')

        # --- DEBUG LOGS ---
        # Verifique o terminal do 'runserver' após submeter o formulário
        print(f"--- DEBUG CLEAN METHOD ---")
        print(f"Valor CPF (limpo): {cpf} (Tipo: {type(cpf)})")
        print(f"Valor Passaporte (limpo): {passaporte} (Tipo: {type(passaporte)})")
        # --------------------

        # --- REGRA 1: NÃO AMBOS (Anti-Autofill) ---
        if cpf and passaporte:
            print("DEBUG: ERRO - Ambos os campos (CPF e Passaporte) estão preenchidos.")
            # Este é o erro que você deveria estar vendo.
            raise forms.ValidationError(
                'Forneça apenas o CPF ou o Passaporte, não ambos. Apague o campo preenchido automaticamente pelo navegador.'
            )

        # --- REGRA 2: PELO MENOS UM ---
        if not cpf and not passaporte:
            print("DEBUG: ERRO - Nenhum documento foi preenchido.")
            raise forms.ValidationError(
                'É obrigatório fornecer um CPF ou um número de Passaporte.'
            )
            
        # Se o código chegou aqui, significa que APENAS UM dos campos foi preenchido.
        # Agora podemos verificar a unicidade com segurança.

        # --- REGRA 3: UNICIDADE (se CPF foi usado) ---
        if cpf:
            print(f"DEBUG: Verificando unicidade do CPF {cpf}...")
            query = Hospede.objects.filter(cpf=cpf)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                print("DEBUG: ERRO - CPF duplicado encontrado.")
                self.add_error('cpf', "Este CPF já está cadastrado para outro hóspede.")

        # --- REGRA 4: UNICIDADE (se Passaporte foi usado) ---
        if passaporte:
            print(f"DEBUG: Verificando unicidade do Passaporte {passaporte}...")
            query = Hospede.objects.filter(passaporte=passaporte)
            if self.instance and self.instance.pk:
                query = query.exclude(pk=self.instance.pk)
            if query.exists():
                self.add_error('passaporte', "Este Passaporte já está cadastrado para outro hóspede.")
        
        return cleaned_data