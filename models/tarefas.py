from database import conectar

CAMPOS = ["id", "funcionario", "funcao", "local", "tarefa",
          "prioridade", "status", "inicio_dt", "termino_dt",
          "responsavel_registro", "dt_criacao"]

class Tarefas:

    def __init__(self, funcionario, funcao, local, tarefa, prioridade,
                 status, inicio_dt, termino_dt, responsavel_registro,
                 dt_criacao, id=None):
        self.id                   = id
        self.funcionario          = funcionario
        self.funcao               = funcao
        self.local                = local
        self.tarefa               = tarefa
        self.prioridade           = prioridade
        self.status               = status
        self.inicio_dt            = inicio_dt
        self.termino_dt           = termino_dt
        self.responsavel_registro = responsavel_registro
        self.dt_criacao           = dt_criacao

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO tarefas
                (funcionario, funcao, local, tarefa, prioridade, status,
                 inicio_dt, termino_dt, responsavel_registro, dt_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.funcionario, self.funcao, self.local, self.tarefa,
              self.prioridade, self.status, self.inicio_dt, self.termino_dt,
              self.responsavel_registro, self.dt_criacao))
        conexao.commit()
        conexao.close()

    @staticmethod
    def atualizar_status(id_tarefa, novo_status):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(
            "UPDATE tarefas SET status = ? WHERE id = ?",
            (novo_status, id_tarefa)
        )
        conexao.commit()
        conexao.close()

    @staticmethod
    def excluir(id_tarefa):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        conexao.commit()
        conexao.close()

    @staticmethod
    def listar_todas():
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM tarefas")
        linhas  = cursor.fetchall()
        conexao.close()
        return [dict(zip(CAMPOS, linha)) for linha in linhas]

    @staticmethod
    def buscar_por_id(id_tarefa):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM tarefas WHERE id = ?", (id_tarefa,))
        linha   = cursor.fetchone()
        conexao.close()
        if linha:
            return dict(zip(CAMPOS, linha))
        return None