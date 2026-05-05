import os  # Biblioteca nativa do Python para lidar com caminhos de pastas
from flask import Flask, send_from_directory
from flask_cors import CORS
from db.database import criar_banco

# Blueprints
from routes.tarefas_routes import tarefas_bp
from routes.funcionarios_routes import funcionarios_bp
from routes.salas_routes import salas_bp
from routes.registro_routes import registros_bp

app = Flask(__name__)
CORS(app)

criar_banco()

# --- CONFIGURAÇÃO DOS CAMINHOS ---
# 1. Pega o caminho absoluto da pasta onde este arquivo (app.py) está (ou seja, a pasta 'backend')
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))

# 2. Volta uma pasta (..) e entra na pasta 'frontend'
DIRETORIO_FRONTEND = os.path.join(DIRETORIO_ATUAL, '..', 'frontend')
# ---------------------------------

app.register_blueprint(tarefas_bp)
app.register_blueprint(funcionarios_bp)
app.register_blueprint(salas_bp)
app.register_blueprint(registros_bp)

# --- ROTAS PARA O FRONT-END ---
@app.route("/login")
def login_page():
    # Agora passamos a variável DIRETORIO_FRONTEND que sabe exatamente onde os arquivos estão
    return send_from_directory(DIRETORIO_FRONTEND, "login.html")

@app.route("/")
def index():
    return send_from_directory(DIRETORIO_FRONTEND, "index.html")

@app.route("/salas")
def salas_pages():
    return send_from_directory(DIRETORIO_FRONTEND, "salas.html")

@app.route("/relatorio")
def registros_pages():
    return send_from_directory(DIRETORIO_FRONTEND, "relatorio.html")

# 🚀 Start
if __name__ == "__main__":
    app.run(debug=True, port=5000)