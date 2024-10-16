import os
import zipfile
import logging
import subprocess
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import socket
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import paramiko

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

# Carregar chave secreta do ambiente
secret_key = os.getenv('SECRET_KEY').encode()
cipher = Fernet(secret_key)

# Funções de criptografia e descriptografia
def decrypt(encrypted_data: str) -> str:
    """Descriptografa uma string."""
    return cipher.decrypt(encrypted_data.encode()).decode()

# Informações sensíveis (encriptadas previamente)
SFTP_PASSWORD = decrypt(os.getenv('SFTP_PASSWORD'))
DB_PASSWORD = decrypt(os.getenv('DB_PASSWORD'))
SMTP_PASSWORD = decrypt(os.getenv('SMTP_PASSWORD'))

# Configurações de SFTP e diretórios
sftp_host = ''
sftp_username = ''
remote_directory_path = ''

local_directory_path = '/'
extract_dir = '/'
backup_file_name = ''
extracted_file_path = os.path.join(extract_dir, backup_file_name)

# Configurações do banco de dados PostgreSQL
db_name = ''
db_user = ''
db_host = ''
db_port = ''

# Configurações de log e e-mail
log_file_path = ''
recipient_email = ''
smtp_server = ''
smtp_port = 587

def is_network_available():
    """Verifica se a rede está disponível."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def send_email(subject, body, attachment_path=None):
    """Envia um e-mail com ou sem anexo."""
    logging.info("Preparando o e-mail para envio.")
    msg = MIMEMultipart()
    msg['From'] = sftp_username  # Usando o nome de usuário do SMTP
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    if attachment_path:
        try:
            with open(attachment_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
                msg.attach(part)
            logging.info(f"Anexo {attachment_path} adicionado ao e-mail.")
        except Exception as e:
            logging.error(f"Erro ao anexar arquivo: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sftp_username, SMTP_PASSWORD)
            server.send_message(msg)
            logging.info("E-mail enviado com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar o e-mail: {e}")

def download_latest_backup():
    """Faz o download do backup mais recente do servidor SFTP."""
    start_time = time.time()
    logging.info("Iniciando o download do backup.")
    try:
        transport = paramiko.Transport((sftp_host, 22))
        transport.connect(username=sftp_username, password=SFTP_PASSWORD)
        sftp = paramiko.SFTPClient.from_transport(transport)

        remote_files = sftp.listdir(remote_directory_path)
        matching_files = [f for f in remote_files if f.startswith('cli_emp00509-dberp-') and f.endswith('.zip')]

        if not matching_files:
            logging.error("Nenhum arquivo de backup encontrado.")
            return None

        latest_backup_file = max(matching_files, key=lambda f: f)
        local_file_path = os.path.join(local_directory_path, latest_backup_file)

        sftp.get(os.path.join(remote_directory_path, latest_backup_file), local_file_path)
        logging.info(f"Backup baixado para {local_file_path}.")

        sftp.close()
        transport.close()

        duration = time.time() - start_time
        logging.info(f"Tempo de download: {int(duration // 60)} minutos e {duration % 60:.2f} segundos.")
        return local_file_path
    except Exception as e:
        logging.error(f"Erro ao baixar o backup: {e}")
        return None

def unzip_file(zip_file_path, extract_to):
    """Descompacta o arquivo ZIP baixado."""
    start_time = time.time()
    logging.info(f"Descompactando {zip_file_path}.")
    try:
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            file_list = zip_ref.namelist()
            if not any(backup_file_name in file for file in file_list):
                logging.error(f"O ZIP não contém o backup necessário.")
                return False, []

            zip_ref.extractall(extract_to)
            logging.info(f"Arquivo descompactado em {extract_to}.")
            return True, zip_ref.namelist()
    except Exception as e:
        logging.error(f"Erro ao descompactar: {e}")
        return False, []

def delete_local_file(file_path):
    """Deleta um arquivo local."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.info(f"{file_path} deletado com sucesso.")
        else:
            logging.warning(f"{file_path} não encontrado.")
    except Exception as e:
        logging.error(f"Erro ao deletar {file_path}: {e}")

def restore_backup_to_db(backup_file_path):
    """Restaura o backup no banco de dados PostgreSQL."""
    start_time = time.time()
    logging.info(f"Restaurando {backup_file_path} no banco de dados.")
    try:
        restore_command = [
            'pg_restore', '--host', db_host, '--port', db_port,
            '--username', db_user, '--dbname', db_name, '--clean',
            '--no-owner', '--no-privileges', '-v', backup_file_path
        ]
        env = os.environ.copy()
        env['PGPASSWORD'] = DB_PASSWORD
        subprocess.run(restore_command, env=env, check=True)
        logging.info("Backup restaurado com sucesso.")
    except Exception as e:
        logging.error(f"Erro na restauração: {e}")

def main():
    """Função principal que executa todo o processo de backup e restauração."""
    while True:
        if is_network_available():
            logging.info("Rede disponível. Iniciando download.")
            local_file_path = download_latest_backup()

            if local_file_path and zipfile.is_zipfile(local_file_path):
                unzip_success, extracted_files = unzip_file(local_file_path, extract_dir)
                if unzip_success:
                    delete_local_file(local_file_path)
                    restore_backup_to_db(extracted_file_path)

                    for extracted_file in extracted_files:
                        delete_local_file(os.path.join(extract_dir, extracted_file))

                    send_email("Processo Completo", "Backup restaurado com sucesso.", log_file_path)
                    break
            else:
                logging.warning("Arquivo ZIP inválido.")
        else:
            logging.warning("Rede indisponível. Tentando novamente em 30 minutos.")
            time.sleep(1800)

if __name__ == "__main__":
    main()
