#acript para criar novas senhas criptografadas se necessário.
from config.crypto_utils import encrypt

# Exemplo de senhas a serem criptografadas
sftp_password = encrypt("CkEfTB9DGR")
db_password = encrypt("nev@litelec@m")
smtp_password = encrypt("syfd743mdm2h")

print(f"SFTP Password Criptografado: {sftp_password}")
print(f"DB Password Criptografado: {db_password}")
print(f"SMTP Password Criptografado: {smtp_password}")
