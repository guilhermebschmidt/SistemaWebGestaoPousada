from django.db import models
from django.core.exceptions import ValidationError
from datetime import date


class Hospede(models.Model):
    cpf = models.CharField(max_length=100, primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255, verbose_name="Endereço")

    def clean(self):
        hoje = date.today()

        if self.data_nascimento > hoje:
            raise ValidationError("A data de nascimento não pode ser futura.")

        if self.data_nascimento.year >= hoje.year:
            raise ValidationError("A data de nascimento não pode ser no ano atual ou em anos futuros.")

        idade = hoje.year - self.data_nascimento.year - (
            (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day)
        )
        if idade < 18:
            raise ValidationError("O hóspede deve ter 18 anos ou mais.")

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'hospede'
        verbose_name = 'Hóspede'
        verbose_name_plural = 'Hóspedes'
