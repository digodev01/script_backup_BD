
# **Backup e Restauração Automática de Banco de Dados PostgreSQL via SFTP**  

Este projeto automatiza o processo de **download, descompactação e restauração** de backups de um banco de dados PostgreSQL. A solução se conecta a um servidor SFTP, baixa o backup mais recente, descompacta o arquivo e restaura os dados no banco de dados configurado. Além disso, o script envia notificações por e-mail com logs do processo e verifica a disponibilidade de rede antes de iniciar o processo.

---

## **Funcionalidades**
- **Conexão segura via SFTP**: Faz o download do backup mais recente de um servidor remoto.
- **Descompactação automática**: Descompacta arquivos ZIP contendo backups.
- **Restauração do banco de dados PostgreSQL**: Usa `pg_restore` para restaurar o banco.
- **Envio de notificações por e-mail**: Envia um e-mail com logs e status de execução.
- **Monitoramento de rede**: Só executa o processo se a rede estiver disponível.
- **Logs detalhados**: Todos os eventos e erros são registrados para acompanhamento.

---

## **Pré-requisitos**

1. **Sistema Operacional**  
   - Linux (Debian/Ubuntu recomendado)  
   - Testado em ambientes com PostgreSQL e SFTP configurados.  

2. **Dependências Python**  
   ```bash
   pip install paramiko
   ```
    ## Verificação de Outras Dependências

As seguintes bibliotecas e módulos são **integrados ao Python** e **não precisam ser instalados separadamente**:

- **Bibliotecas Padrão:**
  - `smtplib`: Biblioteca para envio de e-mails via protocolo SMTP.
  - `os`: Funções relacionadas ao sistema operacional (manipulação de arquivos, caminhos, etc.).
  - `time`: Manipulação de tempo e cronômetros.
  - `socket`: Comunicação em rede e verificação de disponibilidade de conexão.
  - `logging`: Registro de logs para depuração e monitoramento.

- **Módulos Internos:**
  - `zipfile`: Manipulação de arquivos no formato ZIP.
  - `subprocess`: Execução de comandos do sistema diretamente via Python.

Essas dependências são nativas e vêm com qualquer instalação do Python (versão 3.x ou superior). Por isso, **não é necessário instalá-las manualmente com `pip`**.

3. **PostgreSQL**  
   - O **pg_restore** deve estar disponível no PATH do sistema.

4. **Servidor SFTP**  
   - Acesso ao servidor SFTP com um usuário e senha válidos.

---

## **Configuração**  

1. **Clonar o Repositório**  
   ```bash
   git clone https://github.com/seu_usuario/seu_projeto.git
   cd seu_projeto
   ```

2. **Configurar as Variáveis**  
   Edite as seguintes configurações no script:

   ```python
   # Configurações de SFTP
   sftp_host = '200.125.129.90'
   sftp_username = 'backup_erp'

   # Configurações locais
   local_directory_path = '/home/nevoli/Documentos/'

   # Banco de Dados PostgreSQL
   db_name = 'nevoli_DB'
   db_user = 'postgres'
   db_host = '10.1.133.6'

   # Configurações de E-mail
   smtp_server = 'server18.mailgrid.com.br'
   smtp_username = 'nevolitelecom@nevolitelecom.com.br'
   ```

---
3. **Criptografia e descriptografia de senhas**
**Observação:** As senhas devem ser criptografadas antes de serem armazenadas no arquivo `.env`. Utilize o método de criptografia fornecido pelo seu projeto para gerar essas senhas

## Chave Secreta

O arquivo `secret.key` contém a chave utilizada para a criptografia e descriptografia das senhas. Este arquivo deve ser mantido em um local seguro e **não deve ser compartilhado publicamente**.

## Como Funciona

### Carregamento das Variáveis de Ambiente

O script utiliza a biblioteca [`python-dotenv`](https://pypi.org/project/python-dotenv/) para carregar as variáveis de ambiente definidas no arquivo `.env`.

A chave secreta é carregada da variável de ambiente `SECRET_KEY` e utilizada para criar um objeto `Fernet` da biblioteca [`cryptography`](https://cryptography.io/en/latest/).

### Descriptografia das Senhas

As senhas de SFTP, banco de dados e SMTP são recuperadas do ambiente, descriptografadas e atribuídas às variáveis correspondentes.

### Exemplo de Uso

No seu script principal (por exemplo, `main.py`), você pode usar as variáveis descriptografadas para se conectar ao SFTP, ao banco de dados ou ao servidor SMTP conforme necessário.

```python
from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet

# Carregar variáveis de ambiente
load_dotenv()

# Carregar a chave secreta
with open("secret.key", "rb") as key_file:
    secret_key = key_file.read()

cipher = Fernet(secret_key)

# Descriptografar as senhas
SFTP_PASSWORD = cipher.decrypt(os.getenv("SFTP_PASSWORD").encode()).decode()
DB_PASSWORD = cipher.decrypt(os.getenv("DB_PASSWORD").encode()).decode()
SMTP_PASSWORD = cipher.decrypt(os.getenv("SMTP_PASSWORD").encode()).decode()

# Exemplo de uso das senhas descriptografadas
print("Senha SFTP:", SFTP_PASSWORD)
print("Senha do Banco de Dados:", DB_PASSWORD)
print("Senha SMTP:", SMTP_PASSWORD)

## **Como Executar o Projeto**

1. **Verificar Conectividade**  
   Certifique-se de que a internet e o servidor SFTP estão acessíveis.

2. **Executar o Script**  
   ```bash
   python backup_script.py
   ```

4. **Acompanhar os Logs**  
   Os logs são salvos em:  
   `/home/nevoli/Documentos/logs/cron_script_bkp.log`

---

## **Descrição das Funções**

- **is_network_available()**: Verifica a internet.  
- **download_latest_backup()**: Baixa o backup do SFTP.  
- **unzip_file()**: Descompacta o arquivo ZIP.  
- **restore_backup_to_db()**: Restaura o banco de dados.  
- **send_email()**: Envia e-mails com logs.  

---

## **Personalização**

- **Alterar diretórios**: Edite os caminhos locais no script.
- **Agendar Execução Automática**:  
   Adicione ao `crontab` para rodar às 2h da manhã:  
   ```bash
   crontab -e
   ```
   ```bash
   0 2 * * * /usr/bin/python3 /caminho/para/backup_script.py
   ```

---

5. **Problemas e Soluções Possíveis**

lista possíveis **erros, causas e soluções** para o script de automação envolvendo SFTP, PostgreSQL e envio de e-mails.

---

## 1.1 Problemas com Credenciais e Variáveis de Ambiente

### Possíveis Causas:
- **Chave incorreta:** A chave `SECRET_KEY` usada para descriptografar senhas pode estar errada ou corrompida.
- **Variáveis ausentes:** Variáveis de ambiente como `SFTP_PASSWORD`, `DB_PASSWORD` ou `SMTP_PASSWORD` podem não estar definidas no `.env`.
- **Inconsistência de criptografia:** Mudanças na chave podem corromper as senhas já criptografadas.

### Erro Provável:
```plaintext
InvalidToken na função decrypt.
```

### Soluções:
- Verificar se a chave `SECRET_KEY` corresponde à utilizada para criptografar os dados.
- Garantir que todas as variáveis sensíveis estão definidas no arquivo `.env`.
- Reencriptar as senhas, se necessário, para garantir consistência.

---

## 2.1 Problemas de Rede e Conectividade

### Possíveis Causas:
- **Falta de conectividade com a internet:** O script pode falhar ao acessar SFTP ou SMTP.
- **IP do SFTP inacessível:** O servidor `200.125.129.90` pode estar fora do ar ou bloqueado.
- **Problema de DNS:** Falha na resolução de nomes para o banco ou servidor SMTP.
- **Porta bloqueada:** Firewall pode impedir o acesso às portas 22 (SFTP) ou 587 (SMTP).

### Erro Provável:
```plaintext
OSError: [Errno 101] Network is unreachable.
```

### Soluções:
- Testar a conectividade manualmente usando `ping` ou `telnet`.
- Verificar firewall e permissões de rede.
- Consultar o administrador da rede para resolver bloqueios.

---

## 3.1 Problemas de Download e Descompactação

### Possíveis Causas:
- **Arquivo não encontrado no SFTP:** O nome esperado não corresponde ao padrão.
- **Download parcial:** Arquivo corrompido devido a falha na rede.
- **ZIP inválido:** Função `zipfile.is_zipfile()` falha em ZIPs corrompidos.
- **Permissão insuficiente:** O script pode não ter acesso ao diretório `/home/nevoli/Documentos/`.

### Erros Prováveis:
- **`FileNotFoundError`** ao tentar acessar arquivos inexistentes.
- **`BadZipFile`** ao tentar descompactar um ZIP corrompido.

### Soluções:
- Validar manualmente a presença dos arquivos no SFTP.
- Garantir que o diretório de destino tenha as permissões corretas.
- Implementar verificação de integridade do arquivo após download.

---

## 4.1 Problemas na Restauração do Banco de Dados

### Possíveis Causas:
- **Banco inacessível:** O banco `nevoli_DB` pode estar offline ou com credenciais incorretas.
- **Timeout de conexão:** O servidor pode estar sobrecarregado.
- **Backup incompatível:** O arquivo pode não ser compatível com `pg_restore`.
- **Erros de permissão:** O usuário `postgres` pode não ter as permissões necessárias.
- **Conflito de dados:** Dados duplicados podem causar falhas na restauração.

### Erro Provável:
```plaintext
subprocess.CalledProcessError durante a execução do pg_restore.
```

### Soluções:
- Verificar credenciais e permissões de banco de dados.
- Testar a restauração manualmente para validar o formato do backup.
- Limpar dados antigos do banco, se necessário, para evitar conflitos.

---

## 5.1 Problemas no Envio de E-mails

### Possíveis Causas:
- **Falha de autenticação:** Usuário ou senha SMTP estão incorretos.
- **Porta SMTP bloqueada:** O envio pela porta 587 pode ser bloqueado por firewall.
- **Anexo inválido:** O arquivo de log pode não existir ou estar corrompido.
- **Destinatário inválido:** O e-mail pode ser rejeitado pelo servidor.

### Erros Prováveis:
- **`SMTPAuthenticationError`** se houver falha na autenticação.
- **`smtplib.SMTPException`** para problemas gerais no envio.

### Soluções:
- Testar envio de e-mails manualmente com as mesmas credenciais.
- Verificar a presença do arquivo de anexo antes do envio.
- Usar outras portas SMTP (como 465) ou consultar o administrador de rede.

---

## 6.1 Problemas de Segurança

### Possíveis Riscos:
- **Exposição de credenciais:** O arquivo `.env` pode expor senhas e chaves se não for protegido.
- **Senha visível em memória:** O uso de `env['PGPASSWORD']` pode deixar a senha exposta.
- **Ataques Man-in-the-Middle:** Se o SMTP não usar TLS, as credenciais podem ser interceptadas.

---

## 7.1 Outros Problemas Gerais

### Possíveis Causas:
- **Logs ausentes:** O diretório `/home/nevoli/Documentos/logs/` pode não existir.
- **Loop infinito:** Se a rede estiver sempre indisponível, o script pode entrar em loop.
- **Execução paralela:** Se o script rodar em paralelo, pode haver conflitos de acesso a arquivos.

### Erros Prováveis:
- **`PermissionError`** se o script não puder criar ou modificar arquivos.
- **Uso excessivo de CPU:** Loop contínuo pode sobrecarregar o sistema.

### Soluções:
- Garantir que o diretório de logs exista antes da execução.
- Implementar controle para evitar execuções paralelas.
- Limitar o número de tentativas em caso de falha na rede.

---

## Conclusão

Este documento destaca os principais problemas que podem ocorrer ao rodar o script e sugere possíveis soluções. A **identificação rápida de erros e uma abordagem sistemática de solução** são essenciais para garantir a estabilidade da aplicação. O código é totalmente comandando pela função "

---

### Checklist de Prevenção
- [ ] Testar conectividade com SFTP e SMTP antes da execução.
- [ ] Validar a consistência das variáveis de ambiente.
- [ ] Verificar permissões de arquivos e diretórios.
- [ ] Realizar testes manuais de restauração do banco.
- [ ] Garantir que o diretório de logs esteja acessível.


---

## **Contribuições**

1. Crie um fork do projeto.  
2. Crie uma nova branch:  
   ```bash
   git checkout -b minha-feature
   ```
3. Commit das mudanças:  
   ```bash
   git commit -am 'Adicionando minha nova feature'
   ```
4. Push para o branch:  
   ```bash
   git push origin minha-feature
   ```
5. Abra um Pull Request no GitHub.

---

## **Contato**

- **E-mail**: sistemas@nevolitelecom.com.br  
- **Website**: [Nevoli Telecom](https://www.nevolitelecom.com.br)  
