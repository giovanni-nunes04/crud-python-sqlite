import sqlite3

def conectar():
    return sqlite3.connect('app.db')

def criar_banco():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nome        TEXT    NOT NULL,
            rg          TEXT    NOT NULL UNIQUE,
            cpf         TEXT    NOT NULL UNIQUE,
            telefone    TEXT    NOT NULL,
            email       TEXT    NOT NULL UNIQUE,
            cargo       TEXT    NOT NULL,
            endereco    TEXT    NOT NULL,
            senha       TEXT    NOT NULL,
            dt_criacao  DATE    NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id                   INTEGER   PRIMARY KEY AUTOINCREMENT,
            funcionario          TEXT      NOT NULL,
            funcao               TEXT      NOT NULL,
            local                TEXT      NOT NULL,
            tarefa               TEXT      NOT NULL,
            prioridade           TEXT      NOT NULL,
            status               TEXT      NOT NULL,
            inicio_dt            TIMESTAMP NOT NULL,
            termino_dt           TIMESTAMP NOT NULL,
            responsavel_registro TEXT      NOT NULL,
            dt_criacao           DATE      NOT NULL
        )
    ''')

    conexao.commit()
    conexao.close()

if __name__ == '__main__':
    criar_banco()