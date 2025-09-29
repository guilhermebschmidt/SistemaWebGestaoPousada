from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from ..models.reserva import Reserva # Importando o modelo de reserva

# Renderiza os templates de e-mail e envia a confirmação para o hóspede
def enviar_email_confirmacao(reserva: Reserva):
    assunto = f"Sua reserva na Pousada foi confirmada! (Nº {reserva.id})"
    email_remetente = settings.DEFAULT_FROM_EMAIL
    email_destinatario = [reserva.id_hospede.email]
    contexto = {'reserva': reserva}
    
    corpo_html = render_to_string('core/emails/confirmacao_reserva.html', contexto)
    corpo_texto = render_to_string('core/emails/confirmacao_reserva.txt', contexto)

    email = EmailMultiAlternatives(assunto, corpo_texto, email_remetente, email_destinatario)
    email.attach_alternative(corpo_html, "text/html")
    email.send()