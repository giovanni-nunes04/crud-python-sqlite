# 📋 Sistema de Gestão Operacional

Sistema web para controle de **tarefas** e **funcionários**, desenvolvido com Flask (Python) no backend e HTML/CSS/JS puro no frontend, utilizando SQLite como banco de dados.

---

## 🗂️ Estrutura do Projeto

```
projeto/
├── app.py                      # Ponto de entrada da aplicação Flask
├── database.py                 # Conexão e criação das tabelas SQLite
├── validator.py                # Validações de campos e entidades
├── index.html                  # Interface web (frontend)
├── requirements.txt            # Dependências Python
│
├── models/
│   ├── __init__.py
│   ├── tarefas.py              # Model da tabela tarefas
│   └── funcionarios.py         # Model da tabela funcionarios
│
└── routes/
    ├── __init__.py
    ├── tarefas_routes.py       # Rotas/endpoints de tarefas
    └── funcionarios_routes.py  # Rotas/endpoints de funcionários
```

---

## ⚙️ Tecnologias Utilizadas

| Camada     | Tecnologia                        |
|------------|-----------------------------------|
| Backend    | Python 3.11+ / Flask 3.1          |
| Banco de dados | SQLite 3 (via módulo padrão)  |
| Frontend   | HTML5 / CSS3 / JavaScript (Vanilla) |
| CORS       | Flask-CORS 5.0                    |
| Fontes     | IBM Plex Mono + Syne (Google Fonts) |

---

## 🚀 Como Executar

### 1. Pré-requisitos

- Python 3.11 ou superior
- pip

### 2. Instalação das dependências

```bash
pip install -r requirements.txt
```

### 3. Iniciar o servidor

```bash
python app.py
```

O servidor irá subir em `http://localhost:5000`.

### 4. Acessar o sistema

Abra o navegador e acesse:

```
http://localhost:5000
```

---

## 🗃️ Banco de Dados

O banco `app.db` é criado automaticamente na primeira execução. Duas tabelas são geradas:

### Tabela `tarefas`

| Coluna                | Tipo      | Descrição                        |
|-----------------------|-----------|----------------------------------|
| id                    | INTEGER   | Chave primária (autoincrement)   |
| funcionario           | TEXT      | Nome do funcionário              |
| funcao                | TEXT      | Função/cargo do responsável      |
| local                 | TEXT      | Local de execução                |
| tarefa                | TEXT      | Descrição da tarefa              |
| prioridade            | TEXT      | `baixa` / `media` / `alta`       |
| status                | TEXT      | `pendente` / `em andamento` / `concluida` / `cancelada` |
| inicio_dt             | TIMESTAMP | Data/hora de início              |
| termino_dt            | TIMESTAMP | Data/hora de término             |
| responsavel_registro  | TEXT      | Quem registrou a tarefa          |
| dt_criacao            | DATE      | Data de criação do registro      |

### Tabela `funcionarios`

| Coluna      | Tipo    | Descrição                             |
|-------------|---------|---------------------------------------|
| id          | INTEGER | Chave primária (autoincrement)        |
| nome        | TEXT    | Nome completo                         |
| rg          | TEXT    | RG (único, somente dígitos, 7–9 chars) |
| cpf         | TEXT    | CPF (único, 11 dígitos)               |
| telefone    | TEXT    | Telefone (8–15 dígitos)               |
| email       | TEXT    | E-mail (único)                        |
| cargo       | TEXT    | Cargo/função                          |
| endereco    | TEXT    | Endereço completo                     |
| senha       | TEXT    | Senha (mín. 8 chars, maiúsc., minúsc. e número) |
| dt_criacao  | DATE    | Data de criação do registro           |

---

## 🔌 API — Endpoints

### Tarefas — `/api/tarefas`

| Método   | Rota                  | Descrição                    |
|----------|-----------------------|------------------------------|
| `GET`    | `/api/tarefas`        | Lista todas as tarefas       |
| `GET`    | `/api/tarefas/<id>`   | Busca uma tarefa por ID      |
| `POST`   | `/api/tarefas`        | Cadastra uma nova tarefa     |
| `PUT`    | `/api/tarefas/<id>`   | Atualiza o status da tarefa  |
| `DELETE` | `/api/tarefas/<id>`   | Exclui uma tarefa            |

#### Exemplo — POST `/api/tarefas`

```json
{
  "funcionario": "Carlos Silva",
  "funcao": "Técnico",
  "local": "Setor B",
  "tarefa": "Verificar equipamentos",
  "prioridade": "alta",
  "status": "pendente",
  "inicio_dt": "2025-01-15 08:00",
  "termino_dt": "2025-01-15 17:00",
  "responsavel_registro": "Ana Lima",
  "dt_criacao": "2025-01-14"
}
```

#### Exemplo — PUT `/api/tarefas/<id>`

```json
{
  "status": "concluida"
}
```

---

### Funcionários — `/api/funcionarios`

| Método   | Rota                       | Descrição                          |
|----------|----------------------------|------------------------------------|
| `GET`    | `/api/funcionarios`        | Lista todos os funcionários        |
| `GET`    | `/api/funcionarios/<id>`   | Busca um funcionário por ID        |
| `POST`   | `/api/funcionarios`        | Cadastra um novo funcionário       |
| `PUT`    | `/api/funcionarios/<id>`   | Atualiza dados do funcionário      |
| `DELETE` | `/api/funcionarios/<id>`   | Exclui um funcionário              |

#### Exemplo — POST `/api/funcionarios`

```json
{
  "nome": "Ana Lima",
  "rg": "1234567",
  "cpf": "12345678901",
  "telefone": "11999999999",
  "email": "ana.lima@empresa.com",
  "cargo": "Analista",
  "endereco": "Rua das Flores, 100, São Paulo",
  "senha": "Senha@123",
  "dt_criacao": "2025-01-14"
}
```

#### Exemplo — PUT `/api/funcionarios/<id>`

Envie apenas os campos que deseja alterar:

```json
{
  "cargo": "Analista Sênior",
  "telefone": "11988887777"
}
```

---

## ✅ Validações

Todas as entradas passam pelo `validator.py` antes de chegar ao banco.

### Regras por campo

| Campo      | Regra                                                        |
|------------|--------------------------------------------------------------|
| `nome`     | Somente letras e espaços                                     |
| `cpf`      | Exatamente 11 dígitos numéricos                              |
| `rg`       | Entre 7 e 9 dígitos numéricos                                |
| `telefone` | Entre 8 e 15 dígitos numéricos                               |
| `email`    | Formato válido `usuario@dominio.com`                         |
| `cargo`    | Letras, números e espaços                                    |
| `endereco` | Letras, números, espaços e `, . -`                           |
| `senha`    | Mín. 8 caracteres, ao menos 1 maiúscula, 1 minúscula, 1 dígito |
| `prioridade` | `baixa`, `media` ou `alta`                               |
| `status`   | `pendente`, `em andamento`, `concluida` ou `cancelada`       |

### Resposta de erro (HTTP 400)

```json
{
  "erros": [
    "Campo 'cpf': CPF inválido (somente 11 dígitos).",
    "Campo 'senha': Senha fraca (mín. 8 chars, maiúscula, minúscula e número)."
  ]
}
```

---

## 🖥️ Interface Web

A interface é composta por uma sidebar com navegação dividida em dois módulos:

### Módulo Tarefas
- **Painel** — cards de resumo (total, concluídas, em andamento, prioridade alta, pendentes e funcionários) + tabela das últimas tarefas
- **Consultar** — tabela completa com busca em tempo real e ações de editar/excluir por linha
- **Cadastrar** — formulário completo com todos os campos obrigatórios
- **Atualizar** — lista para seleção + modal de atualização de status
- **Excluir** — lista com modal de confirmação antes da exclusão

### Módulo Funcionários
- **Consultar** — tabela com nome, CPF, RG, telefone, e-mail, cargo, endereço e busca em tempo real
- **Cadastrar** — formulário completo com validação de senha
- **Atualizar** — modal com campos editáveis (nome, telefone, e-mail, cargo, endereço e senha opcional)
- **Excluir** — modal de confirmação com dados do funcionário antes de excluir

---

## 📁 Configuração do Editor (VSCode)

Para resolver o aviso `Import could not be resolved` do Pylance, o projeto inclui `.vscode/settings.json`:

```json
{
  "python.analysis.extraPaths": ["."]
}
```

---

## 📦 Dependências (`requirements.txt`)

```
flask==3.1.0
flask-cors==5.0.1
```

> `sqlite3` e `re` fazem parte da biblioteca padrão do Python e não precisam ser instalados.

---

## 📌 Observações

- A senha dos funcionários **não é retornada** nas respostas GET por segurança.
- O CPF é verificado quanto à **duplicidade** no momento do cadastro.
- O banco `app.db` é criado automaticamente — não é necessário nenhuma migração manual.
- O frontend consome a API em `http://localhost:5000/api` — certifique-se de que o servidor Flask está rodando antes de abrir o `index.html`.