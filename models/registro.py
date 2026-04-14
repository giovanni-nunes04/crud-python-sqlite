from database import conectar
import bcrypt

CAMPOS = ["id", "usuario", "senha", "data_acesso"]

class Registro:

    def __init__(self, usuario, senha, data_acesso, id=None):
        self.id          = id
        self.usuario     = usuario
        self.senha       = senha
        self.data_acesso = data_acesso

    @staticmethod
    def gerar_hash(senha):
        return bcrypt.hashpw(
            senha.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    @staticmethod
    def verificar_senha(senha_digitada, senha_hash):
        return bcrypt.checkpw(
            senha_digitada.encode('utf-8'),
            senha_hash.encode('utf-8')
        )

    def salvar(self):
        conexao = conectar()
        cursor  = conexao.cursor()

        senha_hash = self.gerar_hash(self.senha)

        cursor.execute('''
            INSERT INTO registro
                (usuario, senha, data_acesso)
            VALUES (?, ?, ?)
        ''', (self.usuario, senha_hash, self.data_acesso))

        conexao.commit()
        conexao.close()

    @staticmethod
    def atualizar(id_registro, dados: dict):
        campos_permitidos = ["usuario", "senha", "data_acesso"]
        sets    = []
        valores = []

        for campo in campos_permitidos:
            if campo in dados:
                # 🔐 Se for senha, criptografa antes
                if campo == "senha":
                    dados[campo] = Registro.gerar_hash(dados[campo])

                sets.append(f"{campo} = ?")
                valores.append(dados[campo])

        if not sets:
            return

        valores.append(id_registro)

        conexao = conectar()
        cursor  = conexao.cursor()

        cursor.execute(
            f"UPDATE registro SET {', '.join(sets)} WHERE id = ?",
            valores
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

        cursor.execute("SELECT * FROM registro")
        linhas = cursor.fetchall()

        conexao.close()
        return [dict(zip(CAMPOS, linha)) for linha in linhas]

    @staticmethod
    def buscar_por_id(id_registro):
        conexao = conectar()
        cursor  = conexao.cursor()

        cursor.execute("SELECT * FROM registro WHERE id = ?", (id_registro,))
        linha = cursor.fetchone()

        conexao.close()

        if linha:
            return dict(zip(CAMPOS, linha))
        return None

    @staticmethod
    def buscar_por_usuario(usuario: str):
        conexao = conectar()
        cursor  = conexao.cursor()

        cursor.execute("SELECT * FROM registro WHERE usuario = ?", (usuario,))
        linha = cursor.fetchone()

        conexao.close()

        if linha:
            return dict(zip(CAMPOS, linha))
        return None

    @staticmethod
    def autenticar(usuario, senha_digitada):
        registro = Registro.buscar_por_usuario(usuario)

        if not registro:
            return False

        senha_hash = registro["senha"]

        return Registro.verificar_senha(senha_digitada, senha_hash)