from django.db import models
from django.core.exceptions import ValidationError
from apps.core.models import Hospede
from .categoria import Categoria 

class Titulo(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('boleto', 'Boleto'),
        ('pix', 'PIX'),
        ('cartao', 'Cartão'),
        ('dinheiro', 'Dinheiro'),
        ('transferencia', 'Transferência'),
        ('outro', 'Outro'),
    ]

    tipo_documento = models.CharField(
        max_length=30,
        choices=TIPO_DOCUMENTO_CHOICES,
        verbose_name="Tipo de Documento"
    )
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    conta_corrente = models.CharField(max_length=100, verbose_name="Conta Corrente")
    
    cancelado = models.BooleanField(verbose_name="Cancelado", default=False)
    pago = models.BooleanField(default=False, null=False, verbose_name="Pago")
    
    tipo = models.BooleanField(default=True, verbose_name="Tipo") # True=Entrada, False=Saída
    
    reserva = models.ForeignKey(
        'core.Reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Reserva",
        related_name='titulos'
    )
    hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Hóspede")
    
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='titulos',
        null=True,
        blank=True,
        verbose_name="Categoria"
    )

    data = models.DateField(verbose_name="Data de Emissão")
    data_pagamento = models.DateField(null=True, blank=True, verbose_name="Data de Pagamento")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_compensacao = models.DateField(null=True, blank=True, verbose_name="Data de Compensação")

    observacao = models.TextField(null=True, blank=True, verbose_name="Observação")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        status = "[CANCELADO]" if self.cancelado else ("[PAGO]" if self.pago else "[ABERTO]")
        return f"{status} {self.descricao} - R$ {self.valor}"

    class Meta:
        db_table = "financeiro_titulo"
        verbose_name = "Título Financeiro"
        verbose_name_plural = "Títulos Financeiros"
        ordering = ['-data_vencimento']

    def tipo_display(self):
        return "Entrada" if self.tipo else "Saída"

    def clean(self):
        if self.cancelado and self.pago:
            raise ValidationError("Um título não pode estar 'Pago' e 'Cancelado' ao mesmo tempo. Se foi cancelado, não deve receber baixa.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)