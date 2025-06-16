from django.db import models


class Quarto(models.Model):
    numero = models.CharField(max_length=100)
    status = models.BooleanField(default=True)
    descricao = models.TextField(max_length=100)
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