#script para descriptografar as senhas geradas.
import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Função para carregar a chave
def load_key():
    """Carrega a chave secreta do ambiente."""
    return os.getenv('SECRET_KEY').encode()

# Função para descriptografar a senha
def decrypt_password(encrypted_data: str) -> str:
    """Descriptografa uma string."""
    cipher = Fernet(load_key())
    return cipher.decrypt(encrypted_data.encode()).decode()

# Exemplo de uso
if __name__ == "__main__":
    # Obtendo a senha criptografada da variável de ambiente
    encrypted_password = os.getenv('SMTP_PASSWORD')
    
    if encrypted_password:
        # Descriptografando a senha
        try:
            decrypted_password = decrypt_password(encrypted_password)
            print("Senhas descriptografadas:", decrypted_password)
        except Exception as e:
            print(f"Erro ao descriptografar a senha: {e}")
    else:
        print("A variável de ambiente 'SMTP_PASSWORD' não está definida.")

