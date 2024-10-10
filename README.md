# script_backup_BD
script feito para fazer uma restauração de um backup do banco de dados de um servidor remoto para o banco de dados da empresa Nevoli telecom
# Automação de Download e Restauração de Backup PostgreSQL

Este script em Python automatiza o processo de download, extração e restauração de backups de banco de dados PostgreSQL a partir de um servidor remoto SFTP. Ele monitora a disponibilidade da rede e faz novas tentativas automaticamente se a rede estiver indisponível.

## Funcionalidades

- **Integração com SFTP**: Conecta-se de forma segura a um servidor remoto SFTP para baixar o backup mais recente do banco de dados.
- **Manipulação de Arquivos ZIP**: Valida, extrai e processa arquivos ZIP que contêm o backup do banco de dados.
- **Restauração Automática do PostgreSQL**: Restaura o backup baixado diretamente em um banco de dados PostgreSQL local ou remoto.
- **Registro de Logs**: Mantém um log detalhado do processo, incluindo erros e tempos de execução.
- **Notificações por Email**: Envia uma notificação por e-mail com o log após a conclusão do processo, seja ele bem-sucedido ou não.
- **Resiliência de Rede**: Só inicia o download quando a rede estiver disponível, tentando novamente periodicamente caso a rede esteja fora do ar.

## Configuração e Instalação

### Pré-requisitos

- Python 3.x
- PostgreSQL instalado na máquina onde o script será executado
- Credenciais de acesso ao servidor SFTP
- O comando `pg_restore` deve estar disponível no sistema (no PATH)

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seuusuario/automacao-backup-postgresql.git
   cd automacao-backup-postgresql
   Instale as bibliotecas Python necessárias:

pip install paramiko
Configure o script:

Atualize as informações de conexão com o servidor SFTP no script (sftp_host, sftp_username, etc.)
Atualize os detalhes de conexão com o banco de dados PostgreSQL (db_name, db_user, etc.)
Configure as credenciais de e-mail e o destinatário para envio das notificações.

2. Executando o Script
Execute o script com:

python3 backup_automation.py
O script fará automaticamente:

Verificação da disponibilidade da rede.
Download do arquivo de backup mais recente do servidor remoto SFTP.
Descompactação do backup.
Restauração do backup no banco de dados PostgreSQL.
Envio de e-mail com o arquivo de log após a conclusão.

Licença
Este projeto está licenciado sob a licença MIT.
