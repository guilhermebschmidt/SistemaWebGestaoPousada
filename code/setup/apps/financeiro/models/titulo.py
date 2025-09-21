from django.db import models
from apps.core.models import Hospede#, Reserva
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
    cancelado = models.BooleanField(verbose_name="Cancelado")
    tipo = models.BooleanField(default=True, verbose_name="Tipo")
    # Relações
    #reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Reserva")
    reserva = models.ForeignKey(
        'core.Reserva',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Reserva"
    )
    hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Hóspede")

    # Datas
    data = models.DateField(verbose_name="Data de Emissão")
    data_pagamento = models.DateField(null=True, blank=True, verbose_name="Data de Pagamento")
    data_vencimento = models.DateField(verbose_name="Data de Vencimento")
    data_compensacao = models.DateField(null=True, blank=True, verbose_name="Data de Compensação")

    # Sugestões extras
    observacao = models.TextField(null=True, blank=True, verbose_name="Observação")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.descricao} - {self.valor} ({self.get_situacao_display()})"

    class Meta:
        db_table = "financeiro_titulo"
        verbose_name = "Título Financeiro"
        verbose_name_plural = "Títulos Financeiros"

    def tipo_display(self):
        return "Entrada" if self.tipo else "Saída"
