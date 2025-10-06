from django.db import models


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
    
    descricao = models.TextField(max_length=100)
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
    

    class Meta:
        db_table = 'quarto'