from django.db import models

class Banco(models.Model):
    descricao = models.CharField(max_length=255, verbose_name="Descrição")
    codigo    = models.CharField(max_length=10, verbose_name="Código", unique=True)

    def __str__(self):
      return f"{self.codigo} - {self.descricao}"

    class Meta:
      db_table = "financeiro_banco"
      verbose_name = "Banco"
      verbose_name_plural = "Bancos"
      ordering = ["codigo"]
