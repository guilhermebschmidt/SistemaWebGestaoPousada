from django.db import models
from decimal import Decimal


class Quarto(models.Model):
    numero = models.CharField(max_length=100)
    
    STATUS_CHOICES = (
        ('DISPONIVEL', 'Disponível'),
        ('OCUPADO', 'Ocupado'),
        ('MANUTENCAO', 'Em Manutenção'),
    )
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='DISPONIVEL',
        verbose_name='Status'
    )

    TIPOS_QUARTOS_CHOICES = (
        ('SUITE', 'Quarto Suite'),
        ('TERREO', 'Chalé Térreo'),
        ('LOFT', 'Chalé Loft'),
        ('FLAT', 'Flat'),
    )
    tipo_quarto = models.CharField(
        max_length=15,
        choices=TIPOS_QUARTOS_CHOICES,
        default='SUITE',
        verbose_name='Tipo de Quarto'
    )

    descricao = models.TextField(max_length=100, blank=True)
    capacidade = models.PositiveSmallIntegerField(
        verbose_name='Capacidade',
        help_text='Número máximo de pessoas que o quarto acomoda.'
    )

    preco = models.DecimalField(
        verbose_name='Preço',
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    def __str__(self):
        return f"Quarto {self.numero}"

    def is_available(self, data_inicio, data_fim, reserva_a_ignorar=None):
        """Verifica se este quarto está disponível no período [data_inicio, data_fim).

        Retorna True se estiver disponível, False se houver conflito com reservas
        cujo status seja bloqueante.
        """
        # import local para evitar dependência circular em nível de import
        from .reserva import Reserva

        STATUS_BLOQUEANTES = ['CONFIRMADA', 'ATIVA', 'CONCLUIDA']
        conflitos = Reserva.objects.filter(
            id_quarto=self,
            data_reserva_inicio__lt=data_fim,
            data_reserva_fim__gt=data_inicio,
            status__in=STATUS_BLOQUEANTES,
        )
        if reserva_a_ignorar and getattr(reserva_a_ignorar, 'pk', None):
            conflitos = conflitos.exclude(pk=reserva_a_ignorar.pk)
        return not conflitos.exists()
    
