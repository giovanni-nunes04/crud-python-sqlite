from database import conectar

CAMPOS = ["id", "criador_id", "funcionario", "funcao", "local", "tarefa", 
          "prioridade", "status", "inicio_dt", "termino_dt", "responsavel_registro", "dt_criacao"]

class Tarefas:
    
    @staticmethod
    def salvar(dados: dict):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO tarefas (criador_id, funcionario, funcao, local, tarefa, prioridade, status, inicio_dt, termino_dt, responsavel_registro, dt_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            dados['criador_id'], dados['funcionario'], dados['funcao'], 
            dados['local'], dados['tarefa'], dados['prioridade'], 
            dados['status'], dados['inicio_dt'], dados['termino_dt'], 
            dados['responsavel_registro'], dados['dt_criacao']
        ))
        conexao.commit()
        conexao.close()

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

    @staticmethod
    def listar_todas():
        """Lista todas as tarefas para o painel principal"""
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM tarefas ORDER BY id DESC")
        linhas  = cursor.fetchall()
        conexao.close()
        return [dict(zip(CAMPOS, linha)) for linha in linhas]

    @staticmethod
    def atualizar(id_tarefa, dados: dict):
        """Atualiza campos permitidos de uma tarefa"""
        if not dados:
            return
        conexao = conectar()
        cursor  = conexao.cursor()
        sets    = ", ".join(f"{k} = ?" for k in dados.keys())
        valores = list(dados.values()) + [id_tarefa]
        cursor.execute(f"UPDATE tarefas SET {sets} WHERE id = ?", valores)
        conexao.commit()
        conexao.close()

    @staticmethod
    def excluir(id_tarefa):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("DELETE FROM tarefas WHERE id = ?", (id_tarefa,))
        conexao.commit()
        conexao.close()