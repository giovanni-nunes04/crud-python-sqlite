import sqlite3
import hashlib
from werkzeug.security import generate_password_hash
import datetime

def conectar():
    return sqlite3.connect('app.db')

def criar_banco():
    conexao = conectar()
    cursor  = conexao.cursor()

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
            dt_criacao  DATE    NOT NULL,
            is_admin    INTEGER DEFAULT 0 
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tarefas (
            id                   INTEGER   PRIMARY KEY AUTOINCREMENT,
            criador_id           INTEGER   NOT NULL,
            funcionario          TEXT      NOT NULL,
            funcao               TEXT      NOT NULL,
            local                TEXT      NOT NULL,
            tarefa               TEXT      NOT NULL,
            prioridade           TEXT      NOT NULL,
            status               TEXT      NOT NULL,
            inicio_dt            TIMESTAMP NOT NULL,
            termino_dt           TIMESTAMP NOT NULL,
            responsavel_registro TEXT      NOT NULL,
            dt_criacao           DATE      NOT NULL,
            FOREIGN KEY (criador_id) REFERENCES funcionarios (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS salas (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            criador_id  INTEGER NOT NULL,
            funcionario TEXT    NOT NULL,
            sala        TEXT    NOT NULL,
            status      TEXT    NOT NULL,
            data_uso    DATE    NOT NULL,
            inicio_hr   TIME    NOT NULL,
            termino_hr  TIME    NOT NULL,
            dt_criacao  DATE    NOT NULL,
            FOREIGN KEY (criador_id) REFERENCES funcionarios (id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS log_logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            data_login DATE NOT NULL,
            hora_login TIME NOT NULL
        )
    ''')

    cursor.execute("SELECT id FROM funcionarios WHERE is_admin = 1")
    if not cursor.fetchone():
        senha_admin = generate_password_hash("admin123")
        cpf_admin = hashlib.sha256("00000000000".encode()).hexdigest()
        rg_admin = hashlib.sha256("000000000".encode()).hexdigest()
        tel_admin = hashlib.sha256("00000000000".encode()).hexdigest()
        
        cursor.execute('''
            INSERT INTO funcionarios (nome, rg, cpf, telefone, email, cargo, endereco, senha, dt_criacao, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', ("Admin Master", rg_admin, cpf_admin, tel_admin, "admin@sistema.com", "Master", "Sede", senha_admin, datetime.date.today(), 1))

    conexao.commit()
    conexao.close()

if __name__ == '__main__':
    criar_banco()