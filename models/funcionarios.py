from database import conectar
from werkzeug.security import generate_password_hash
import hashlib

CAMPOS = ["id", "nome", "rg", "cpf", "telefone",
          "email", "cargo", "endereco", "senha", "dt_criacao", "is_admin"]

def hash_dado(dado: str) -> str:
    """Gera um hash irreversível (SHA-256) para CPFs, RGs e Telefones"""
    return hashlib.sha256(str(dado).encode()).hexdigest()

class Funcionarios:

    def __init__(self, nome, rg, cpf, telefone, email,
                 cargo, endereco, senha, dt_criacao, is_admin=0, id=None):
        self.id         = id
        self.nome       = nome
        self.rg         = hash_dado(rg) if len(rg) < 60 else rg
        self.cpf        = hash_dado(cpf) if len(cpf) < 60 else cpf
        self.telefone   = hash_dado(telefone) if len(telefone) < 60 else telefone
        self.email      = email
        self.cargo      = cargo
        self.endereco   = endereco
        self.senha      = generate_password_hash(senha) if not senha.startswith('scrypt') else senha
        self.dt_criacao = dt_criacao
        self.is_admin   = is_admin

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO funcionarios
                (nome, rg, cpf, telefone, email, cargo, endereco, senha, dt_criacao, is_admin)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.nome, self.rg, self.cpf, self.telefone, self.email,
              self.cargo, self.endereco, self.senha, self.dt_criacao, self.is_admin))
        conexao.commit()
        conexao.close()

    @staticmethod
    def atualizar(id_funcionario, dados: dict):
        campos_permitidos = ["nome", "telefone", "email", "cargo", "endereco", "senha"]
        sets   = []
        valores = []
        for campo in campos_permitidos:
            if campo in dados:
                sets.append(f"{campo} = ?")
                # Se for telefone ou senha, aplica o hash antes de atualizar
                if campo == "telefone":
                    valores.append(hash_dado(dados[campo]))
                elif campo == "senha":
                    valores.append(generate_password_hash(dados[campo]))
                else:
                    valores.append(dados[campo])

        if not sets:
            return

        valores.append(id_funcionario)
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(f"UPDATE funcionarios SET {', '.join(sets)} WHERE id = ?", valores)
        conexao.commit()
        conexao.close()

    @staticmethod
    def excluir(id_funcionario):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("DELETE FROM funcionarios WHERE id = ?", (id_funcionario,))
        conexao.commit()
        conexao.close()

    @staticmethod
    def listar_todos():
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios")
        linhas  = cursor.fetchall()
        conexao.close()
        return [dict(zip(CAMPOS, linha)) for linha in linhas]

    @staticmethod
    def buscar_por_id(id_funcionario):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE id = ?", (id_funcionario,))
        linha   = cursor.fetchone()
        conexao.close()
        if linha:
            return dict(zip(CAMPOS, linha))
        return None

    @staticmethod
    def buscar_por_cpf_original(cpf_original: str):
        cpf_hash = hash_dado(cpf_original)
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf_hash,))
        linha   = cursor.fetchone()
        conexao.close()
        if linha:
            return dict(zip(CAMPOS, linha))
        return None