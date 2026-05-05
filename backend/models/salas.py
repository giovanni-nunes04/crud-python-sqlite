from db.database import conectar
from datetime import datetime, date

CAMPOS = ["id", "criador_id", "funcionario", "sala", "status", "data_uso",
          "inicio_hr", "termino_hr", "dt_criacao"]

class Salas:

    SALAS_DISPONIVEIS = [
        "Sala de Reunião 01",
        "Sala de Reunião 02",
        "Sala de Conferência",
        "Auditório",
    ]

    def __init__(self, criador_id, funcionario, sala, data_uso, inicio_hr, termino_hr,
                 status="reservada", id=None, dt_criacao=None):
        self.id          = id
        self.criador_id  = criador_id
        self.funcionario = funcionario
        self.sala        = sala
        self.status      = status           
        self.data_uso    = data_uso
        self.inicio_hr   = inicio_hr
        self.termino_hr  = termino_hr
        self.dt_criacao  = dt_criacao or str(date.today())

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO salas
                (criador_id, funcionario, sala, status, data_uso,
                 inicio_hr, termino_hr, dt_criacao)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (self.criador_id, self.funcionario, self.sala, self.status, self.data_uso,
              self.inicio_hr, self.termino_hr, self.dt_criacao))
        conexao.commit()
        conexao.close()

    @staticmethod
    def sincronizar_status():
        """
        Chamado antes de qualquer listagem.
        - Exclui reservas cujo dia/hora de término já passou.
        - Marca como 'em uso' as que estão dentro do intervalo agora.
        - Garante 'reservada' para as futuras (caso relógio atrase, etc.)
        """
        agora       = datetime.now()
        hoje        = agora.strftime("%Y-%m-%d")
        hora_atual  = agora.strftime("%H:%M")

        conexao = conectar()
        cursor  = conexao.cursor()

        cursor.execute('''
            DELETE FROM salas
            WHERE data_uso < ?
               OR (data_uso = ? AND termino_hr <= ?)
        ''', (hoje, hoje, hora_atual))

        cursor.execute('''
            UPDATE salas SET status = 'em uso'
            WHERE data_uso = ?
              AND inicio_hr <= ?
              AND termino_hr >  ?
        ''', (hoje, hora_atual, hora_atual))

        cursor.execute('''
            UPDATE salas SET status = 'reservada'
            WHERE data_uso = ?
              AND inicio_hr > ?
        ''', (hoje, hora_atual))

        cursor.execute('''
            UPDATE salas SET status = 'reservada'
            WHERE data_uso > ?
        ''', (hoje,))

        conexao.commit()
        conexao.close()

    @staticmethod
    def verificar_conflito(sala, data_uso, inicio_hr, termino_hr, excluir_id=None):
        """
        Retorna True se já existe uma reserva para a mesma sala/dia
        com horário sobreposto.
        """
        conexao = conectar()
        cursor  = conexao.cursor()

        query  = '''
            SELECT id FROM salas
            WHERE sala     = ?
              AND data_uso = ?
              AND inicio_hr  < ?
              AND termino_hr > ?
        '''
        params = [sala, data_uso, termino_hr, inicio_hr]

        if excluir_id:
            query  += " AND id != ?"
            params.append(excluir_id)

        cursor.execute(query, params)
        resultado = cursor.fetchone()
        conexao.close()
        return resultado is not None

    @staticmethod
    def atualizar(id_salas, campos: dict):
        if not campos:
            return
        conexao    = conectar()
        cursor     = conexao.cursor()
        set_clause = ", ".join(f"{k} = ?" for k in campos)
        valores    = list(campos.values()) + [id_salas]
        cursor.execute(f"UPDATE salas SET {set_clause} WHERE id = ?", valores)
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
        Salas.sincronizar_status()          
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(
            "SELECT * FROM salas ORDER BY data_uso, inicio_hr"
        )
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
        return dict(zip(CAMPOS, linha)) if linha else None