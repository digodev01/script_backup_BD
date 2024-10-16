import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket
import time

# Configurações do SMTP
smtp_server = 'server18.mailgrid.com.br'
smtp_port = 587
smtp_username = 'nevolitelecom@nevolitelecom.com.br'  # Seu e-mail do servidor SMTP
smtp_password = 'syfd743mdm2h'  # Senha do servidor SMTP

recipient_email = 'rodrigodesantana1234@gmail.com'
attachment_file_path = 'C:/Users/Suporte/Documents/teste.txt'  # Caminho para o arquivo a ser anexado

# Função para verificar a conectividade com a internet
def is_network_available():
    try:
        # Tentando se conectar ao DNS público do Google (8.8.8.8)
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

# Função para enviar o e-mail com anexo
def send_email_with_attachment():
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = 'Teste de Envio de E-mail com Anexo'

    body = 'Este é um teste de envio de e-mail com um anexo.'
    msg.attach(MIMEText(body, 'plain'))

    # Anexar o arquivo
    try:
        with open(attachment_file_path, 'rb') as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename={attachment_file_path.split("/")[-1]}')
            msg.attach(part)

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {attachment_file_path}")
        return

    # Enviar o e-mail
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Inicia a comunicação segura
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")

# Loop para verificar a rede e enviar o e-mail
def main():
    while True:
        if is_network_available():
            print("Rede disponível. Tentando enviar o e-mail.")
            send_email_with_attachment()
            break  # Sai do loop após o envio do e-mail com sucesso
        else:
            print("Rede não disponível. Tentando novamente em 30 minutos.")
            time.sleep(1800)  # Aguarda 30 minutos antes de tentar novamente

if __name__ == "__main__":
    main()
