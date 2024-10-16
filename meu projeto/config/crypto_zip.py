import os
import logging
from cryptography.fernet import Fernet
from dotenv import load_dotenv

# Carrega as variáveis do .env
load_dotenv()

def load_key():
    """Carrega a chave secreta da variável de ambiente."""
    key = os.getenv('SECRET_KEY')
    if not key:
        raise ValueError("SECRET_KEY não encontrada no .env ou nas variáveis de ambiente.")
    return Fernet(key)

cipher = load_key()

def encrypt_zip_file(zip_file_path):
    """Criptografa um arquivo ZIP."""
    try:
        with open(zip_file_path, 'rb') as f:
            data = f.read()

        encrypted_data = cipher.encrypt(data)
        encrypted_path = zip_file_path + ".enc"

        with open(encrypted_path, 'wb') as f:
            f.write(encrypted_data)

        logging.info(f"Arquivo {zip_file_path} criptografado como {encrypted_path}.")
        return encrypted_path
    except Exception as e:
        logging.error(f"Erro ao criptografar o arquivo ZIP: {e}")

def decrypt_zip_file(encrypted_file_path, output_path):
    """Descriptografa um arquivo ZIP criptografado."""
    try:
        with open(encrypted_file_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = cipher.decrypt(encrypted_data)

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        logging.info(f"Arquivo {encrypted_file_path} descriptografado como {output_path}.")
        return output_path
    except Exception as e:
        logging.error(f"Erro ao descriptografar o arquivo ZIP: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Teste: Criptografar e Descriptografar
    original_zip = "C:/Users/Suporte/Documents/dbemp00509_vdi.zip"
    encrypted_zip = encrypt_zip_file(original_zip)

    


