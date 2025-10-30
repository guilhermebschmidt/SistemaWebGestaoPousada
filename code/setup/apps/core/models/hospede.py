from django.db import models
from django.core.exceptions import ValidationError
from datetime import date, datetime
import re

class Hospede(models.Model):
    # -------- Dados Pessoais -------- #
    cpf = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name="CPF")
    passaporte =models.CharField(max_length=15, unique=True, null=True, blank=True,verbose_name="Passaporte")
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField()

    # -------- Dados de Contato -------- #
    telefone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    # -------- Endereço -------- #
    rua = models.CharField(max_length=255, verbose_name="Rua")
    numero = models.CharField(max_length=10, verbose_name="Número")
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Complemento")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")
    cep = models.CharField(max_length=10, verbose_name="CEP")

    def clean(self):
        super().clean()
        hoje = date.today()
        # -------- Validação da Data de Nascimento -------- #
        if isinstance(self.data_nascimento, str):
            try:
                self.data_nascimento = datetime.strptime(self.data_nascimento, "%Y-%m-%d").date()
            except ValueError:
                raise ValidationError("Data de nascimento inválida.")

        if self.data_nascimento:
            if self.data_nascimento > hoje:
                raise ValidationError("A data de nascimento não pode ser futura.")

            idade = hoje.year - self.data_nascimento.year - (
                (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
            )
            if idade < 18:
                raise ValidationError("O hóspede deve ter 18 anos ou mais.")
       
        # -------- Validação do CPF/Passaporte -------- #
        cpf_limpo = re.sub(r'\D', '', self.cpf or '')
        passaporte_limpo = (self.passaporte or '').strip().upper()

        if not cpf_limpo and not passaporte_limpo:
            raise ValidationError('É obrigatório fornecer um CPF ou um número de Passaporte.')

        if cpf_limpo and passaporte_limpo:
            raise ValidationError('Forneça apenas o CPF ou o Passaporte, não ambos.')
        
        self.cpf = cpf_limpo
        self.passaporte = passaporte_limpo


    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'hospede'
        verbose_name = 'Hóspede'
        verbose_name_plural = 'Hóspedes'

    def save(self, *args, **kwargs):
      
        self.full_clean()

        super().save(*args, **kwargs)