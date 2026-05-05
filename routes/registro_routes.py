from flask import Blueprint, jsonify, request
from auth import token_required, admin_required
from models.registro import Registro
from models.log_login import LogLogin
import jwt
import datetime
import os

SECRET_KEY = os.getenv("SECRET_KEY")

registros_bp = Blueprint("registros", __name__, url_prefix="/api/registros")

@registros_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}

    usuario = data.get("usuario", "").strip()
    senha   = data.get("senha", "").strip()

    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400

    user = Registro.autenticar(usuario, senha)

    if not user:
        return jsonify({"erro": "Usuário ou senha incorretos"}), 401

    token = jwt.encode({
        "id": user["id"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=8)
    }, SECRET_KEY, algorithm="HS256")

    try:
        LogLogin.registrar(usuario)
        print("LOG SALVO COM SUCESSO")
    except Exception as e:
        print("ERRO AO SALVAR LOG:", e)

    return jsonify({
        "mensagem": "Login realizado com sucesso",
        "token": token,
        "usuario": usuario
    }), 200


@registros_bp.route("/logs", methods=["GET"])
@token_required
@admin_required
def listar_logs(current_user):
    logs = LogLogin.listar_todos()
    return jsonify(logs), 200

@registros_bp.route("/logs", methods=["DELETE"])
@token_required
@admin_required
def limpar_logs(current_user):
    LogLogin.limpar_todos()
    return jsonify({"mensagem": "Logs limpos com sucesso"}), 200

@registros_bp.route("", methods=["GET"])
def listar():
    return jsonify(Registro.listar_todos()), 200


@registros_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    registro = Registro.buscar_por_id(id)
    if not registro:
        return jsonify({"erro": "Registro não encontrado"}), 404
    return jsonify({"id": registro["id"], "usuario": registro["usuario"]}), 200

@registros_bp.route("", methods=["POST"])
def cadastrar():
    data = request.json or {}

    usuario = data.get("usuario", "").strip()
    senha   = data.get("senha", "").strip()

    if not usuario or not senha:
        return jsonify({"erro": "Usuário e senha são obrigatórios"}), 400

    if len(senha) < 6:
        return jsonify({"erro": "Senha deve ter no mínimo 6 caracteres"}), 400

    if Registro.buscar_por_usuario(usuario):
        return jsonify({"erro": "Usuário já cadastrado"}), 409

    novo = Registro(usuario=usuario, senha=senha)
    novo.salvar()

    return jsonify({"mensagem": "Conta criada com sucesso"}), 201


@registros_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.json or {}

    if not Registro.buscar_por_id(id):
        return jsonify({"erro": "Registro não encontrado"}), 404

    atualizacao = {c: data[c] for c in ["usuario", "senha"] if c in data}

    if not atualizacao:
        return jsonify({"erro": "Nenhum campo válido para atualizar"}), 400

    if "senha" in atualizacao and len(atualizacao["senha"]) < 6:
        return jsonify({"erro": "Senha deve ter no mínimo 6 caracteres"}), 400

    Registro.atualizar(id, atualizacao)

    return jsonify({"mensagem": "Registro atualizado com sucesso"}), 200


@registros_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    if not Registro.buscar_por_id(id):
        return jsonify({"erro": "Registro não encontrado"}), 404

    Registro.excluir(id)

    return jsonify({"mensagem": "Registro excluído com sucesso"}), 200