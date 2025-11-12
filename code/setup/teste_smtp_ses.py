import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Carrega o .env
load_dotenv(dotenv_path="/home/projetos/pousada/code/.env")

SMTP_SERVER = os.getenv("EMAIL_HOST")
SMTP_PORT = int(os.getenv("EMAIL_PORT", 587))
SMTP_USERNAME = os.getenv("EMAIL_HOST_USER")
SMTP_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
TO_EMAIL = os.getenv("TEST_EMAIL")

print("📨 Teste de envio via Amazon SES (usando .env)\n")

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.ehlo()
        server.starttls()  # importante para STARTTLS
        server.ehlo()
        print("🔐 Autenticando...")
        server.login(SMTP_USERNAME, SMTP_PASSWORD)

        print("✅ Login bem-sucedido! Enviando e-mail de teste...")

        # Mensagem segura com UTF-8
        msg = MIMEText("Teste de envio via Amazon SES (arquivo .env). Acentuação ok: é, ç, ã", "plain", "utf-8")
        msg["Subject"] = "Teste SES via .env"
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL

        server.sendmail(FROM_EMAIL, [TO_EMAIL], msg.as_string())
        print("📬 E-mail enviado com sucesso!")

except smtplib.SMTPAuthenticationError as e:
    print("❌ Erro de autenticação SMTP:", e)
except smtplib.SMTPException as e:
    print("❌ Erro SMTP:", e)
except Exception as e:
    print("❌ Erro geral:", e)

