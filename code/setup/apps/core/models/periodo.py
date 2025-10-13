from django.db import models
from django.core.exceptions import ValidationError

class PeriodoAltaTemporada(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome do Período", help_text="Ex: Férias de Verão 2026, Carnaval 2027")
    data_inicio = models.DateField(verbose_name="Data de Início")
    data_fim = models.DateField(verbose_name="Data de Fim")

    def __str__(self):
        return f"{self.nome} ({self.data_inicio.strftime('%d/%m/%Y')} - {self.data_fim.strftime('%d/%m/%Y')})"

    def clean(self):
        if self.data_fim < self.data_inicio:
            raise ValidationError('A data de fim não pode ser anterior à data de início.')

    class Meta:
        verbose_name = "Período de Alta Temporada"
        verbose_name_plural = "Períodos de Alta Temporada"
        ordering = ['data_inicio'] 