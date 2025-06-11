from django.db import models

class Reserva(models.Model):
  id_financeiro = models.IntegerField(verbose_name='ID Financeiro')
  id_hospede = models.IntegerField(verbose_name='ID Hóspede')
  id_quarto = models.IntegerField(verbose_name='ID Quarto')

  data_check_in = models.DateField(verbose_name='Check-in')
  data_check_out = models.DateField(verbose_name='Check-out')
  data_reserva = models.DateField(verbose_name='Data da Reserva')

  valor = models.DecimalField(
    verbose_name='Preço',
    max_digits=10,
    decimal_places=2,
    default=0.00
  )
  def __str__(self):
    return f"Reserva #{self.id} - Hóspede {self.id_hospede} - Quarto {self.id_quarto}"
