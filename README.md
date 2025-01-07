# 📄 **README**

---

# 🚀 **INTRODUÇÃO**

## 📂 **Estrutura do Projeto**

### **Descrição dos Diretórios**

#### **`database/`**  
Contém arquivos relacionados ao banco de dados, como a conexão, operações CRUD, inicialização do banco e scripts SQL.

#### **`models/`**  
Define as tabelas do banco de dados utilizando SQLAlchemy. Cada modelo representa uma entidade no banco de dados, como **departamentos**, **colaboradores**, **cargos** e **usuários**.

#### **`routers/`**  
Contém a lógica de rotas da aplicação FastAPI, dividida por recursos da aplicação para manter as responsabilidades separadas.

#### **`schemas/`**  
Define os esquemas de validação de dados com Pydantic. Essenciais para garantir a consistência de dados entre as entradas de API e a lógica de negócios.

#### **`tests/`**  
Contém testes unitários para garantir que as funcionalidades principais da aplicação estão funcionando conforme esperado.

#### **`main.py`**  
Ponto de entrada principal da aplicação, onde o servidor FastAPI é iniciado.

## 🛠️ **Tecnologias utilizadas**

No projeto foram utilizadas as seguintes tecnologias:

- **Docker e Docker Compose:** Ferramentas essenciais para criar ambientes isolados e consistentes para execução da aplicação, garantindo que a configuração seja facilmente replicável em outros ambientes.
- **Python 3.12:** A linguagem de programação principal do projeto.
- **PostgreSQL 15:** Foi utilizado como banco de dados principal da aplicação.

### 📚 **Bibliotecas**

Lista de bibliotecas utilizadas:

| **Biblioteca**        | **Breve descrição**                                                     |
|------------------------|-------------------------------------------------------------------------|
| **fastapi**            | Framework moderno para a criação de APIs de forma rápida e eficiente.   |
| **sqlalchemy**         | Ferramenta ORM que simplifica a manipulação de dados no banco de dados. |
| **psycopg2-binary**    | Driver PostgreSQL para conectar o app ao banco de dados PostgreSQL.     |
| **pydantic**          | Validação de dados e estruturação de dados no FastAPI.                  |
| **pytest**             | Ferramenta para realização de testes unitários e automação de testes.   |
| **uvicorn**            | Servidor ASGI usado para rodar a aplicação FastAPI                      |
| **sqlalchemy-utils**    | Extensõe para a SQLAlchemy.                                             |
| **requests**           | Biblioteca para realizar chamadas HTTP.                                 |
| **faker**              | Gerador de dados falsos para testes e simulações no banco de dados.     |

## 💡 **Boas práticas**

Durante todo o desenvolvimento do projeto, foram aplicadas boas práticas para garantir um código limpo, legível e fácil de manter:

- **Clean Code:** Prioridade foi dada para um código claro e autoexplicativo, facilitando futuras manutenções.
- **PEP 8:** Seguindo as diretrizes de estilo de código Python.

#### **Padrão de Idioma no Código**

No desenvolvimento deste projeto, **o inglês foi adotado como padrão para nomes de variáveis, funções, classes e outros elementos do código**.

#### **Exceções**
- **Comentários, labels e docstrings**: Estão escritos em **português**, com o objetivo de facilitar o entendimento.

---


## 🏗️ **Estrutura do Banco de Dados**

O projeto utiliza uma estrutura de banco de dados relacional no **PostgreSQL**. Abaixo estão os detalhes da estrutura e relacionamentos:

Os principais modelos/tabelas definem as entidades e seus relacionamentos:

1. **Department**: Representa os departamentos da organização. Cada departamento possui um líder associado.
2. **Employee**: Representa os colaboradores da empresa. Um colaborador pode estar associado a um departamento e um cargo.
3. **Job**: Representa os cargos da empresa. Determina se um colaborador pode ser líder.
4. **User**: Representa os usuários da aplicação, podendo estar vinculados a um colaborador ou serem independentes.

### 🏢 **Regras do banco**

O banco foi modelado com os seguintes comportamentos e regras:

1. **Departamento e Líder:** Cada departamento possui um líder. O relacionamento é gerenciado pela chave estrangeira `leader_id`.
2. **Regras de liderança:** Apenas uma pessoa pode ocupar o cargo de liderança em seu respectivo departamento.
3. **Triggers:** Lógica implementada no banco de dados para garantir consistência nos relacionamentos:
   - **`enforce_leadership_rules`:** Garante que somente uma pessoa pode atuar como líder de um departamento.
   - **`sync_is_leader`:** Atualiza o campo `is_leader` no colaborador ao alterar o campo `leader_id` no departamento.

### 📊 **Estrutura de Tabelas e Relacionamentos**

#### 1. **Tabela `Department`**

- **Descrição:** Contém dados sobre os departamentos da empresa.
- **Campos:** `id`, `name`, `leader_id`
- **Chaves/Relacionamentos:** `leader_id` é chave estrangeira para identificar o líder do departamento (employee).

#### 2. **Tabela `Employee`**

- **Descrição:** Representa os colaboradores da organização.
- **Campos:** `id`, `name`, `last_name`, `register_number`, `job_id`, `department_id`, `salary`,` status`, `is_leader` 
- **Chaves/Relacionamentos:** `job_id` é chave estrangeira para identificar o cargo do colaborador. E `department_id` para identificar o departamento.
  - Cada colaborador está associado a um cargo e a um departamento.
  - O campo `is_leader` indica se o colaborador é o líder de seu respectivo departamento.

#### 3. **Tabela `Job`**

- **Descrição:** Contém informações sobre os cargos dos colaboradores.
- **Campos:** `id`, `name`, `code`, `department_id`, `is_leadership`
- **Chaves/Relacionamentos:**** `department_id` é chave estrangeira para identificar a qual departamento o cargo pertence.
- **Regra importante:** Somente um colaborador pode ocupar um cargo de liderança.

#### 4. **Tabela `User`**

- **Descrição:** Representa os usuários no ambiente da aplicação.
- **Campos:** `id`, `login`, `passw`, `employee_id`,
- **Chaves/Relacionamentos:**** `employee_id` é chave estrangeira para identificar a qual colaborador o usuário está associado.
- **Relacionamentos e condições:**
    - A relação com a tabela `Employee` é opcional.

**Observação Importante:**  
A definição de liderança foi estruturada de forma a garantir que apenas uma pessoa possa atuar como líder para cada departamento, conforme lógica implementada no banco de dados através de **triggers e funções** PostgreSQL.

---


## 📄 **Configuração do Arquivo `.env`**

O arquivo `example.env` contém variáveis de ambiente essenciais para configurar o banco de dados PostgreSQL no ambiente Docker. 
Você pode mudar os parâmetros e adequar o aruivo da maneira que preferir. Abaixo estão os parâmetros utilizados:

| **Chave**               | **Valor**               | **Descrição**                                                                |
|-------------------------|-------------------------|--------------------------------------------------------------------------------|
| `POSTGRES_USER`         | `admin`                | Nome de usuário do PostgreSQL para autenticação no banco de dados.            |
| `POSTGRES_PASSWORD`     | `admin`                | Senha para autenticação no banco.                          |
| `POSTGRES_DB`           | `human_resources_db`    | Nome do banco de dados principal que será criado no PostgreSQL ao iniciar.     |
| `POSTGRES_HOST`         | `db`                   | Nome do container do banco de dados no ambiente Docker Compose.               |
| `POSTGRES_PORT`         | `5432`                 | Porta padrão para conexão com o banco de dados PostgreSQL.                    |

O arquivo `.env` é carregado pelo Docker Compose para configurar o ambiente de execução.

---


## 🛠️ **COMO USAR**

### **Instalação do Docker e do Docker Compose na máquina**

#### **SE VOCÊ JÁ TEM O DOCKER E DOCKER COMPOSE INSTALADO, PULE ESSA ETAPA!**

Para instalar o **Docker** e o **Docker Compose** em distribuições Linux, siga os passos:

#### **1. Atualize seu sistema:**
```bash
sudo apt update && sudo apt upgrade -y
```

#### **2. Instale o Docker:**
```bash
sudo apt install docker.io -y
```

#### **3. Habilite o serviço Docker e inicie:**
```bash
sudo systemctl enable docker
sudo systemctl start docker
```

#### **4. Instale o Docker Compose:**
```bash
sudo apt install docker-compose -y
```

#### **5. Verifique se foi instalado corretamente:**
```bash
docker --version
docker-compose --version
```
**OBS:** Pode ser necessário o sudo e/ou também dependendo da estalação os comandos podem ser sem o hífem:
```bash
docker --version
docker compose --version
```

---

## ✅ **Execução**


### **1. Configurar o ambiente:**

Depois da instalação do Docker, faça uma cópia dentro da própria pasta do projeto, do arquivo .env para alocar as variáveis de ambiente dentro do ambiente Docker com o comando:
```bash
cp example.env .env
```

### 🚀 **2. Executar o ambiente com Docker Compose:**

#### **OBS:** Pode ser necessário executar os comandos abaixo sem o hífen. Exemplo:
```bash
docker compose up
```

Navegue até a pasta do projeto onde está localizado o arquivo docker-compose.yml e execute:
```bash
docker-compose up
```
**OBS:** Pode ser necessário o sudo para executar o docker e docker-compose.

### 📋 **3. Testes:**

Descubra o ID ou nome do container:
```bash
docker ps
```

Para realizar os testes e validar se está tudo "ok":
```bash
docker exec -it <nome_ou_id_do_container> pytest app/tests/
```

Também pode ser executado arquivo por arquivo, com os comandos:
```bash
docker exec -it <nome_ou_id_do_container> pytest app/tests/department_test.py
```
```bash
docker exec -it <nome_ou_id_do_container> pytest app/tests/employee_test.py
```
```bash
docker exec -it <nome_ou_id_do_container> pytest app/tests/job_test.py
```
```bash
docker exec -it <nome_ou_id_do_container> pytest app/tests/user_test.py
```
### ⚠️ **Em casos de erros**

**Caso haja algum erro na execução do aplicativo pelo Docker, você pode tentar subir apenas o PostgreSQL da seguinte forma:**
```bash
docker-compose up db
```

**Após isso, execute o servidor Uvicorn manualmente:**
```bash
uvicorn app.main:app --host 0.0.0.0 --port 5555 --reload
```

**Em caso de erro com as variáveis ambiente que estão no arquivo `.env`, acesso o `conn.py` e defina manualmente**
