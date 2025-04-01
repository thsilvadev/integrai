# [PORTUGUÊS] Assistente WhatsApp com Django e Evolution API

Este projeto é um assistente de WhatsApp construído usando Django, Evolution API, Docker e PostgreSQL. Ele permite que os usuários interajam com um bot no WhatsApp para realizar operações básicas de CRUD, como registrar, editar e excluir dados de usuários. O bot se comunica com os usuários por meio de mensagens no WhatsApp e processa suas solicitações.

## Funcionalidades

- **Registro de Usuário**: Os usuários podem se registrar fornecendo seu nome e email.
- **Gerenciamento de Usuário**: Edite ou exclua dados de usuários por meio de mensagens no WhatsApp.
- **Integração com Webhook**: Lida com mensagens recebidas por meio de um webhook.
- **Evolution API Dockerizada**: Gerencia a comunicação do WhatsApp usando a Evolution API.
- **Banco de Dados PostgreSQL**: Armazena os dados dos usuários de forma segura.

## Como Funciona

1. **Webhook**: A Evolution API envia mensagens recebidas no WhatsApp para o webhook do Django.
2. **Processamento de Mensagens**: O webhook processa a mensagem e determina a ação apropriada (por exemplo, registrar, editar, excluir).
3. **Interação com o Banco de Dados**: Os dados dos usuários são armazenados e gerenciados em um banco de dados PostgreSQL.
4. **Respostas do Bot**: O bot envia respostas de volta ao usuário via WhatsApp.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter os seguintes itens instalados:

- Python 3.8+
- Docker e Docker Compose
- PostgreSQL
- Ngrok (ou qualquer serviço de tunelamento para testar o webhook)

## Instruções de Configuração

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/seu-usuario/assistente-whatsapp.git
   cd assistente-whatsapp
   ```

2. **Configure o Ambiente Virtual**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # No Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure as Variáveis de Ambiente**

   Crie um arquivo `.env` no diretório raiz e adicione as seguintes variáveis:

   ```env
   SERVER_URL=localhost
   INSTANCE=seu_id_da_instancia
   API_KEY=sua_chave_api
   ```

4. **Execute as Migrações**

   Aplique as migrações do banco de dados para configurar o esquema do PostgreSQL:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Inicie o Servidor Django**

   ```bash
   python manage.py runserver
   ```

6. **Inicie a Evolution API**

   Use o Docker Compose para iniciar a Evolution API:

   ```bash
   docker-compose up -d
   ```

7. **Exponha o Webhook**

   Use o Ngrok para expor o webhook na internet:

   ```bash
   ngrok http 8000
   ```

   Atualize o `WEBHOOK_GLOBAL_URL` no arquivo `docker-compose.yml` com a URL do Ngrok.

8. **Teste o Bot**

   Envie uma mensagem no WhatsApp para o bot e interaja com ele para testar a funcionalidade.

## Estrutura do Projeto

- **`users`**: Contém o app Django para gerenciamento de usuários.
  - `models.py`: Define o modelo `User`.
  - `views.py`: Lida com as requisições do webhook.
  - `utils.py`: Funções utilitárias para validação.
  - `actions.py`: Funções para envio de mensagens e gerenciamento de menus.
  - `behaviour.py`: Lógica principal para processar mensagens de usuários.
- **`migrations`**: Arquivos de migração do banco de dados.
- **`docker-compose.yml`**: Configuração para a Evolution API.
- **`manage.py`**: Utilitário de linha de comando do Django.

## Exemplos de Uso

1. **Registrar um Usuário**:
   - Envie uma mensagem: `João Silva, joao.silva@exemplo.com`
   - O bot registrará o usuário e confirmará o registro.

2. **Editar Dados do Usuário**:
   - Envie `1` para editar os dados do usuário.
   - Forneça o novo nome e email quando solicitado.

3. **Excluir Usuário**:
   - Envie `2` para excluir o usuário.
   - Confirme a exclusão respondendo com `SIM`.

## Solução de Problemas

- Certifique-se de que a Evolution API está em execução e acessível.
- Verifique se a URL do webhook está configurada corretamente no arquivo `docker-compose.yml`.
- Confira o arquivo `.env` para garantir que as chaves da API e os detalhes da instância estão corretos.

## Licença

Este projeto está licenciado sob a Licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.

## Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Agradecimentos

- [Django](https://www.djangoproject.com/)
- [Evolution API](https://github.com/AtendAI/Evolution-API)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)

# [ENGLISH] WhatsApp Assistant with Django and Evolution API

This project is a WhatsApp assistant built using Django, Evolution API, Docker, and PostgreSQL. It allows users to interact with a WhatsApp bot for performing basic CRUD operations, such as registering, editing, and deleting user data. The bot communicates with users via WhatsApp messages and processes their requests.

## Features

- **User Registration**: Users can register by providing their name and email.
- **User Management**: Edit or delete user data through WhatsApp messages.
- **Webhook Integration**: Handles incoming messages via a webhook.
- **Dockerized Evolution API**: Manages WhatsApp communication using the Evolution API.
- **PostgreSQL Database**: Stores user data securely.

## How It Works

1. **Webhook**: The Evolution API sends incoming WhatsApp messages to the Django webhook.
2. **Message Processing**: The webhook processes the message and determines the appropriate action (e.g., register, edit, delete).
3. **Database Interaction**: User data is stored and managed in a PostgreSQL database.
4. **Bot Responses**: The bot sends responses back to the user via WhatsApp.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL
- Ngrok (or any tunneling service for webhook testing)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/whatsapp-assistant.git
   cd whatsapp-assistant
   ```

2. **Set Up the Virtual Environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   Create a `.env` file in the root directory and add the following variables:

   ```env
   SERVER_URL=localhost
   INSTANCE=your_instance_id
   API_KEY=your_api_key
   ```

4. **Run Migrations**

   Apply database migrations to set up the PostgreSQL schema:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start the Django Server**

   ```bash
   python manage.py runserver
   ```

6. **Start the Evolution API**

   Use Docker Compose to start the Evolution API:

   ```bash
   docker-compose up -d
   ```

7. **Expose the Webhook**

   Use Ngrok to expose the webhook to the internet:

   ```bash
   ngrok http 8000
   ```

   Update the `WEBHOOK_GLOBAL_URL` in the `docker-compose.yml` file with the Ngrok URL.

8. **Test the Bot**

   Send a WhatsApp message to the bot and interact with it to test the functionality.

## Project Structure

- **`users`**: Contains the Django app for user management.
  - `models.py`: Defines the `User` model.
  - `views.py`: Handles webhook requests.
  - `utils.py`: Utility functions for validation.
  - `actions.py`: Functions for sending messages and managing menus.
  - `behaviour.py`: Core logic for processing user messages.
- **`migrations`**: Database migration files.
- **`docker-compose.yml`**: Configuration for the Evolution API.
- **`manage.py`**: Django's command-line utility.

## Example Usage

1. **Register a User**:
   - Send a message: `John Doe, john.doe@example.com`
   - The bot will register the user and confirm the registration.

2. **Edit User Data**:
   - Send `1` to edit user data.
   - Provide the new name and email when prompted.

3. **Delete User**:
   - Send `2` to delete the user.
   - Confirm the deletion by replying with `SIM`.

## Troubleshooting

- Ensure the Evolution API is running and accessible.
- Verify the webhook URL is correctly configured in the `docker-compose.yml` file.
- Check the `.env` file for correct API keys and instance details.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## Acknowledgments

- [Django](https://www.djangoproject.com/)
- [Evolution API](https://github.com/AtendAI/Evolution-API)
- [Docker](https://www.docker.com/)
- [PostgreSQL](https://www.postgresql.org/)
