from django.db import models
from django.contrib.auth.models import User

class Notificacao(models.Model):
    TIPO_CHOICES = [
        ('reserva', 'Reserva'),
        ('hospede', 'Hóspede'),
        ('financeiro', 'Financeiro'),
        ('aviso', 'Aviso'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True) # Para onde vai ao clicar
    lida = models.BooleanField(default=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='reserva')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"