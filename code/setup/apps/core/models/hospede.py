from django.db import models

class Hospede(models.Model):
    cpf = models.CharField(max_length=100, primary_key=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    data_nascimento = models.DateField()

    def __str__(self):
        return self.nome

    class Meta:
        db_table = 'hospede'
