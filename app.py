from flask import Flask, send_from_directory
from flask_cors import CORS
from database import criar_banco
from routes.tarefas_routes import tarefas_bp
from routes.funcionarios_routes import funcionarios_bp

app = Flask(__name__)
CORS(app)

criar_banco()

app.register_blueprint(tarefas_bp)
app.register_blueprint(funcionarios_bp)

@app.route("/")
def index():
    return send_from_directory(".", "index.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000)