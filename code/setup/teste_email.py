import os
import django
from django.core.mail import send_mail, get_connection

# --- Inicializa o Django ---
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')  # ajuste para seu projeto
django.setup()

# --- Cria a conexão SMTP usando as variáveis de ambiente ---
connection = get_connection(
    backend='django.core.mail.backends.smtp.EmailBackend',
    host=os.getenv('EMAIL_HOST', 'email-smtp.us-east-2.amazonaws.com'),
    port=int(os.getenv('EMAIL_PORT', 587)),
    username=os.getenv('EMAIL_HOST_USER'),
    password=os.getenv('EMAIL_HOST_PASSWORD'),
    use_tls=os.getenv('EMAIL_USE_TLS', 'True') == 'True',
)

# --- Teste de envio ---
try:
    print("🔄 Tentando enviar e-mail via Amazon SES Sandbox...")

    resultado = send_mail(
        subject='Teste SES Sandbox',
        message='Este é um e-mail de teste enviado via Amazon SES Sandbox.',
        from_email=os.getenv('DEFAULT_FROM_EMAIL', 'no-reply@pousadachalesaguadecoco.com.br'),
        recipient_list=['SEU_EMAIL_VERIFICADO_NO_SES@gmail.com'],  # precisa estar verificado no SES
        fail_silently=False,
        connection=connection,
    )

    print(f"✅ E-mails enviados: {resultado}")

except Exception as e:
    print("❌ Erro ao enviar e-mail:", e)

