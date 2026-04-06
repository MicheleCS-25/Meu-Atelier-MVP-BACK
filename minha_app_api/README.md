🚀 Meu Atelier - Backend API

Esta é a API de backend desenvolvida com Flask para gerenciar o estoque de materiais. Ela lida com o armazenamento de dados em SQLite, regras de negócio e fornece uma documentação interativa.

🛠️ Tecnologias e Bibliotecas

Python 3.x: Linguagem base.
Flask: Micro-framework web.
Flask-SQLAlchemy: ORM para manipulação do banco de dados SQLite.
Flasgger (Swagger): Documentação automatizada e interativa da API.
Flask-CORS: Permite que o frontend acesse a API de diferentes origens.

📌 Funcionalidades da API

A API expõe os seguintes endpoints:

GET /: Renderiza a interface principal do sistema.

POST /cadastrar_material: Recebe um JSON com os dados do material e salva no banco.

GET /buscar_materiais: Retorna a lista completa de materiais em formato JSON.

DELETE /deletar_material/<id>: Remove um material específico pelo seu ID.

🗄️ Modelo de Dados (Database)

O banco de dados utiliza SQLite (arquivo database.db) com a seguinte estrutura para a tabela Material:

id: Chave primária (Incremental).

nome_material: Texto único (não permite duplicatas).

data_cadastro: Formato de data (Y-m-d).

quantidade_em_estoque: Valor inteiro.

valor_material: Valor flutuante (decimal).

📖 Documentação Interativa (Swagger)

Uma das grandes vantagens deste backend é a documentação automática. Com o servidor rodando, você pode testar todos os endpoints sem precisar do frontend ou de ferramentas como Postman:

Inicie o servidor: python app.py

Acesse: http://localhost:5000/apidocs/

⚙️ Configuração de Pastas

O código está configurado para buscar os arquivos estáticos e templates em uma estrutura específica:

Templates: ../meu_front/templates

Static: ../meu_front/static

🚀 Como rodar o projeto

Crie um ambiente virtual (venv)

No Mac:
python3 -m venv .venv

Para ativa-lo:
source .venv/bin/activate

Instale as dependências:
pip install -r requirements.txt

Execute a aplicação:
python app.py

O banco de dados será criado automaticamente na primeira execução.

