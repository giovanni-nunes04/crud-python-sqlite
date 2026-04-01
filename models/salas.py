from database import conectar

CAMPOS = ["id", "funcionario", "sala", "status", "data_uso", "inicio_hr",
          "termino_hr", "dt_criacao"]

class Salas:

    def __init__(self, funcionario, status, data_uso, inicio_hr, termino_hr,
                 dt_criacao, id=None):
        self.id                   = id
        self.funcionario          = funcionario
        self.status               = status
        self.data_uso             = data_uso
        self.inicio_hr            = inicio_hr
        self.termino_hr           = termino_hr
        self.dt_criacao           = dt_criacao

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO salas
                (funcionario, status, data_uso,
                 inicio_hr, termino_hr, dt_criacao)
            VALUES (?, ?, ?, ?, ?, ?,)
        ''', (self.funcionario, self.status, self.data_uso, self.inicio_hr,
              self.termino_hr, self.dt_criacao))
        conexao.commit()
        conexao.close()

    @staticmethod
    def atualizar_status(id_salas, novo_status):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(
            "UPDATE salas SET status = ? WHERE id = ?",
            (novo_status, id_salas)
        )
        conexao.commit()
        conexao.close()

    @staticmethod
    def excluir(id_salas):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("DELETE FROM salas WHERE id = ?", (id_salas,))
        conexao.commit()
        conexao.close()

    @staticmethod
    def listar_todas():
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM salas")
        linhas  = cursor.fetchall()
        conexao.close()
        return [dict(zip(CAMPOS, linha)) for linha in linhas]

    @staticmethod
    def buscar_por_id(id_salas):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM salas WHERE id = ?", (id_salas,))
        linha   = cursor.fetchone()
        conexao.close()
        if linha:
            return dict(zip(CAMPOS, linha))
        return None