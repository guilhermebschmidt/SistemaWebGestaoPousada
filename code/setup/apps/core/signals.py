from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Reserva, Hospede, Notificacao

@receiver(post_save, sender=Reserva)
def notificar_nova_reserva(sender, instance, created, **kwargs):
    if created:
        # Notifica todos os administradores/staff
        usuarios = User.objects.filter(is_staff=True)
        # Tenta gerar o link para editar a reserva, se falhar vai para a lista
        try:
            link = reverse('reserva:editar', kwargs={'pk': instance.pk})
        except:
            link = reverse('reserva:list')

        for usuario in usuarios:
            Notificacao.objects.create(
                usuario=usuario,
                titulo=f"Nova Reserva #{instance.id}",
                mensagem=f"Cliente: {instance.id_hospede.nome}",
                link=link,
                tipo='reserva'
            )

@receiver(post_save, sender=Hospede)
def notificar_novo_hospede(sender, instance, created, **kwargs):
    if created:
        usuarios = User.objects.filter(is_staff=True)
        link = reverse('hospede:detalhes', kwargs={'cpf': instance.cpf})
        
        for usuario in usuarios:
            Notificacao.objects.create(
                usuario=usuario,
                titulo="Novo Hóspede",
                mensagem=f"{instance.nome} foi cadastrado.",
                link=link,
                tipo='hospede'
            )