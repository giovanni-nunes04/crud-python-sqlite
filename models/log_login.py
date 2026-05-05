from database import conectar
from datetime import datetime

class LogLogin:

    @staticmethod
    def registrar(usuario):
        conexao = conectar()
        cursor = conexao.cursor()

        agora = datetime.now()

        cursor.execute("""
            INSERT INTO log_logins (usuario, data_login, hora_login)
            VALUES (?, ?, ?)
        """, (
            usuario,
            agora.date().isoformat(),
            agora.strftime("%H:%M:%S")
        ))

        conexao.commit()
        conexao.close()

    @staticmethod
    def listar_todos():
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("""
            SELECT usuario, data_login, hora_login
            FROM log_logins
            ORDER BY data_login DESC, hora_login DESC
        """)

        logs = cursor.fetchall()
        conexao.close()

        return [
            {
                "usuario": row[0],
                "data_login": row[1],
                "hora_login": row[2]
            }
            for row in logs
        ]

    @staticmethod
    def limpar_todos():
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute("DELETE FROM log_logins")

        conexao.commit()
        conexao.close()