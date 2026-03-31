from database import conectar

CAMPOS = ["id", "nome", "rg", "cpf", "telefone",
          "email", "cargo", "endereco", "senha", "dt_criacao"]

class Funcionarios:

    def __init__(self, nome, rg, cpf, telefone, email,
                 cargo, endereco, senha, dt_criacao, id=None):
        self.id         = id
        self.nome       = nome
        self.rg         = rg
        self.cpf        = cpf
        self.telefone   = telefone
        self.email      = email
        self.cargo      = cargo
        self.endereco   = endereco
        self.senha      = senha
        self.dt_criacao = dt_criacao

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO funcionarios
                (nome, rg, cpf, telefone, email, cargo, endereco, senha, dt_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.nome, self.rg, self.cpf, self.telefone, self.email,
              self.cargo, self.endereco, self.senha, self.dt_criacao))
        conexao.commit()
        conexao.close()

    @staticmethod
    def atualizar(id_funcionario, dados: dict):
        """Atualiza os campos informados no dict `dados`."""
        campos_permitidos = ["nome", "telefone", "email",
                             "cargo", "endereco", "senha"]
        sets   = []
        valores = []
        for campo in campos_permitidos:
            if campo in dados:
                sets.append(f"{campo} = ?")
                valores.append(dados[campo])

        if not sets:
            return

        valores.append(id_funcionario)
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(
            f"UPDATE funcionarios SET {', '.join(sets)} WHERE id = ?",
            valores
        )
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
    def buscar_por_cpf(cpf: str):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM funcionarios WHERE cpf = ?", (cpf,))
        linha   = cursor.fetchone()
        conexao.close()
        if linha:
            return dict(zip(CAMPOS, linha))
        return None