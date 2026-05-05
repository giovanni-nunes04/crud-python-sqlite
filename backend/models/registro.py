import bcrypt
from db.database import conectar
from datetime import datetime

CAMPOS_REGISTRO = ["id", "usuario", "senha", "dt_criacao"]
CAMPOS_LOG      = ["id", "usuario", "data_login", "hora_login"]


class Registro:

    def __init__(self, usuario, senha, dt_criacao=None, id=None):
        self.id         = id
        self.usuario    = usuario
        self.senha      = senha
        self.dt_criacao = dt_criacao or datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def gerar_hash(senha: str) -> str:
        return bcrypt.hashpw(
            senha.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    @staticmethod
    def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
        return bcrypt.checkpw(
            senha_digitada.encode("utf-8"),
            senha_hash.encode("utf-8")
        )

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO registro (usuario, senha, dt_criacao)
            VALUES (?, ?, ?)
        ''', (self.usuario, self.gerar_hash(self.senha), self.dt_criacao))
        conexao.commit()
        conexao.close()

    @staticmethod
    def atualizar(id_registro, dados: dict):
        campos_validos = ["usuario", "senha"]
        sets, valores  = [], []

        for campo in campos_validos:
            if campo in dados:
                valor = dados[campo]
                if campo == "senha":
                    valor = Registro.gerar_hash(valor)
                sets.append(f"{campo} = ?")
                valores.append(valor)

        if not sets:
            return

        valores.append(id_registro)
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(
            f"UPDATE registro SET {', '.join(sets)} WHERE id = ?", valores
        )
        conexao.commit()
        conexao.close()

    @staticmethod
    def excluir(id_registro):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("DELETE FROM registro WHERE id = ?", (id_registro,))
        conexao.commit()
        conexao.close()

    @staticmethod
    def listar_todos():
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT id, usuario, dt_criacao FROM registro")
        linhas  = cursor.fetchall()
        conexao.close()
        return [{"id": l[0], "usuario": l[1], "dt_criacao": l[2]} for l in linhas]

    @staticmethod
    def buscar_por_id(id_registro):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM registro WHERE id = ?", (id_registro,))
        linha   = cursor.fetchone()
        conexao.close()
        return dict(zip(CAMPOS_REGISTRO, linha)) if linha else None

    @staticmethod
    def buscar_por_usuario(usuario: str):
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("SELECT * FROM registro WHERE usuario = ?", (usuario,))
        linha   = cursor.fetchone()
        conexao.close()
        return dict(zip(CAMPOS_REGISTRO, linha)) if linha else None

    @staticmethod
    def autenticar(usuario: str, senha_digitada: str) -> bool:
        registro = Registro.buscar_por_usuario(usuario)
        if not registro:
            return False
        return Registro.verificar_senha(senha_digitada, registro["senha"])

class LogLogin:

    @staticmethod
    def registrar(usuario: str):
        """Grava um evento de login bem-sucedido."""
        agora = datetime.now()
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute('''
            INSERT INTO log_logins (usuario, data_login, hora_login)
            VALUES (?, ?, ?)
        ''', (usuario, agora.strftime("%Y-%m-%d"), agora.strftime("%H:%M")))
        conexao.commit()
        conexao.close()

    @staticmethod
    def listar_todos():
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute(
            "SELECT * FROM log_logins ORDER BY id DESC"
        )
        linhas  = cursor.fetchall()
        conexao.close()
        return [dict(zip(CAMPOS_LOG, l)) for l in linhas]

    @staticmethod
    def limpar_todos():
        """Apaga todos os logs (ação administrativa)."""
        conexao = conectar()
        cursor  = conexao.cursor()
        cursor.execute("DELETE FROM log_logins")
        conexao.commit()
        conexao.close()