from django.db import models

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]

    tipo = models.CharField(
        max_length=1,
        choices=TIPO_CHOICES,
        default='D',
        verbose_name='Tipo'
    )

    descricao = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Descrição'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['descricao']

    def __str__(self):
        return self.descricao