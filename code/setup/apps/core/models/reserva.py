from django.db import models
from .hospede import Hospede
from .quarto import Quarto

class Reserva(models.Model):
    #id_financeiro = models.ForeignKey(Financeiro, on_delete=models.CASCADE, verbose_name='Financeiro')
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

    def __str__(self):
        return f"Reserva #{self.id} - Hóspede {self.id_hospede} - Quarto {self.id_quarto}"

    class Meta:
        db_table = 'reserva'
