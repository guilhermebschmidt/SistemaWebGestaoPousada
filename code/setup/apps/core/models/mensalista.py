from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .hospede import Hospede
from .quarto import Quarto

class Mensalista(models.Model):
    hospede = models.OneToOneField(
        Hospede,
        on_delete=models.PROTECT,
        verbose_name="Hóspede"
    )

    quarto = models.ForeignKey(
        Quarto,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        verbose_name="Quarto Fixo"
    )

    valor_mensal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor Mensal Acordado"
    )

    dia_vencimento = models.PositiveSmallIntegerField(
        verbose_name="Dia do Vencimento",
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(31)]
    )

    data_inicio = models.DateField(verbose_name="Data de Início do Contrato")
    
    ativo = models.BooleanField(
        default=True,
        verbose_name="Contrato Ativo?"
    )

    observacoes = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Mensalista"
        verbose_name_plural = "Mensalistas"

    def __str__(self):
        status = "Ativo" if self.ativo else "Inativo"
        return f"{self.hospede.nome} - R$ {self.valor_mensal} ({status})"