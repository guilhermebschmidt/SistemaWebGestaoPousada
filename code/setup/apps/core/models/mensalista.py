from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .hospede import Hospede
from .quarto import Quarto
from datetime import date
from dateutil.relativedelta import relativedelta

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

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        
        mudou_para_inativo = False
        if not is_new:
            try:
                old_instance = Mensalista.objects.get(pk=self.pk)
                if old_instance.ativo and not self.ativo:
                    mudou_para_inativo = True
            except Mensalista.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)

        if is_new:
            self._criar_primeiro_titulo()
        elif mudou_para_inativo:
            self._cancelar_titulos_financeiros()

    def _criar_primeiro_titulo(self):
        from apps.financeiro.models import Titulo

        try:
            primeiro_vencimento = date(self.data_inicio.year, self.data_inicio.month, self.dia_vencimento)
        except ValueError:
            primeiro_vencimento = (self.data_inicio.replace(day=1) + relativedelta(months=1)).replace(day=self.dia_vencimento)

        if primeiro_vencimento < self.data_inicio:
            primeiro_vencimento = primeiro_vencimento + relativedelta(months=1)

        Titulo.objects.create(
            hospede=self.hospede,
            reserva=None,
            descricao=f"Mensalidade (1ª Parcela) - Contrato Mensalista",
            valor=self.valor_mensal,
            data=date.today(),
            data_vencimento=primeiro_vencimento,
            data_pagamento=None,
            tipo=True,
            tipo_documento='boleto',
            conta_corrente='Conta Principal',
            cancelado=False,
            pago=False
        )

    def _cancelar_titulos_financeiros(self):
        from apps.financeiro.models import Titulo
        titulos_mensalidade = Titulo.objects.filter(
            hospede=self.hospede,
            reserva__isnull=True,
            pago=False,
            cancelado=False
        )
        
        for titulo in titulos_mensalidade:
            titulo.cancelado = True
            titulo.save(update_fields=['cancelado'])