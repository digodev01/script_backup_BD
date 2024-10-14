
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
   sftp_host = 'xxxxxxx'
   sftp_username = 'xxxxxxx'
   sftp_password = 'xxxxxx'

   # Configurações locais
   local_directory_path = 'xxxxxxx'

   # Banco de Dados PostgreSQL
   db_name = 'xxxxx'
   db_user = 'xxxxxx'
   db_host = 'xxxxxx'
   db_password = 'xxxxxx'

   # Configurações de E-mail
   smtp_server = 'xxxxxxxxxxxxxx'
   smtp_username = 'xxxxxxxxxx'
   smtp_password = 'xxxxxxxxxxxxx'
   ```

---

## **Como Executar o Projeto**

1. **Verificar Conectividade**  
   Certifique-se de que a internet e o servidor SFTP estão acessíveis.

2. **Executar o Script**  
   ```bash
   python backup_script.py
   ```

3. **Acompanhar os Logs**  
   Os logs são salvos em:  
   `xxxxxxxxxxxxxxxxxxxx`

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

## **Possíveis Problemas e Soluções**

- **Erro de conexão SFTP**: Verifique as credenciais.
- **pg_restore não encontrado**: Instale o PostgreSQL e adicione ao PATH.
- **E-mail não enviado**: Verifique as configurações SMTP.

---

## **Licença**

Distribuído sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

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

- **E-mail**: nevolitelecom@nevolitelecom.com.br  
- **Website**: [Nevoli Telecom](https://www.nevolitelecom.com.br)  

