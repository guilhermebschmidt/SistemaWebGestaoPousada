from django.db import models
from .hospede import Hospede
from .quarto import Quarto
import datetime

class Reserva(models.Model):
    id_hospede = models.ForeignKey(Hospede, on_delete=models.CASCADE, verbose_name='Hóspede')
    id_quarto = models.ForeignKey(Quarto, on_delete=models.CASCADE, verbose_name='Quarto')

    data_check_in = models.DateTimeField(verbose_name='Check-in', null=True, blank=True)
    data_check_out = models.DateTimeField(verbose_name='Check-out', null=True, blank=True)

    data_reserva_inicio = models.DateField(verbose_name='Data início da Reserva', null=True, blank=True)
    data_reserva_fim = models.DateField(verbose_name='Data fim da Reserva', null=True, blank=True)

    quantidade_dias = models.IntegerField(verbose_name='Quantidade de Dias', default=0)

    valor = models.DecimalField(
        verbose_name='Preço',
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    STATUS_CHOICES = (
        ('PREVISTA', 'Prevista'),
        ('ATIVA', 'Ativa'),
        ('CONCLUIDA', 'Concluída'),
        ('CANCELADA', 'Cancelada'),
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PREVISTA',
        null=True
    ) 

    email_confirmacao_enviado = models.BooleanField(default=False)
    
    motivo_cancelamento = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Reserva #{self.id} - Hóspede {self.id_hospede} - Quarto {self.id_quarto}"

    class Meta:
        db_table = 'reserva'

    def save(self, *args, **kwargs):
        old_instance = None
        if self.pk:
            try:
                old_instance = Reserva.objects.get(pk=self.pk)
            except Reserva.DoesNotExist:
                pass

        self.calcular_reserva()

        super().save(*args, **kwargs)

        if old_instance is None:
            self._criar_titulos_financeiros()
        elif self._houve_alteracao_relevante(old_instance):
            self._atualizar_titulos_financeiros()

    def calcular_reserva(self):
        if self.data_reserva_inicio and self.data_reserva_fim and self.id_quarto:
            delta = self.data_reserva_fim - self.data_reserva_inicio
            self.quantidade_dias = delta.days
            valor_diaria_quarto = self.id_quarto.preco
            self.valor = self.quantidade_dias * valor_diaria_quarto
        else:
            self.quantidade_dias = 0
            self.valor = 0.00

    def _criar_titulos_financeiros(self):
        from apps.financeiro.models import Titulo
        if self.valor > 0:
            valor_parcela = self.valor / 2
            today = datetime.date.today()

            Titulo.objects.create(
                reserva=self, hospede=self.id_hospede,
                descricao=f"Sinal (50%) - Reserva #{self.id}",
                valor=valor_parcela, data=today, data_vencimento=today,
                data_pagamento=today, data_compensacao=today + datetime.timedelta(days=1),
                tipo=True, tipo_documento='pix', conta_corrente='Conta Principal',
                cancelado=False
            )
            Titulo.objects.create(
                reserva=self, hospede=self.id_hospede,
                descricao=f"Pagamento Restante - Reserva #{self.id}",
                valor=valor_parcela, data=today, data_vencimento=self.data_reserva_inicio,
                data_pagamento=None, data_compensacao=None,
                tipo=True, tipo_documento='pix', conta_corrente='Conta Principal',
                cancelado=False
            )

    def _atualizar_titulos_financeiros(self):
        from apps.financeiro.models import Titulo
        try:
            titulo_sinal = Titulo.objects.get(reserva=self, descricao__startswith='Sinal')
            titulo_restante = Titulo.objects.get(reserva=self, descricao__startswith='Pagamento Restante')

            if titulo_sinal.data_pagamento is None:
                novo_valor_parcela = self.valor / 2
                titulo_sinal.valor = novo_valor_parcela
                titulo_restante.valor = novo_valor_parcela
                titulo_sinal.save(update_fields=['valor'])
            else:
                titulo_restante.valor = self.valor - titulo_sinal.valor

            titulo_restante.data_vencimento = self.data_reserva_inicio
            titulo_restante.save(update_fields=['valor', 'data_vencimento'])
        except Titulo.DoesNotExist:
            pass

    def _houve_alteracao_relevante(self, old_instance):
        if not old_instance:
            return False
        return (
            old_instance.data_reserva_inicio != self.data_reserva_inicio or
            old_instance.data_reserva_fim != self.data_reserva_fim or
            old_instance.id_quarto != self.id_quarto
        )

   