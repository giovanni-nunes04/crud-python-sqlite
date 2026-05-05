from flask import Blueprint, jsonify, request
from models.funcionarios import Funcionarios
from validator import Validar
from werkzeug.security import check_password_hash
import jwt
import datetime
from auth import token_required, admin_required, SECRET_KEY

funcionarios_bp = Blueprint("funcionarios", __name__, url_prefix="/api/funcionarios")

@funcionarios_bp.route("/login", methods=["POST"])
def login():
    """Rota para autenticar e gerar o Token JWT"""
    data = request.json or {}
    cpf = data.get("cpf")
    senha = data.get("senha")

    if not cpf or not senha:
        return jsonify({"erro": "CPF e senha são obrigatórios"}), 400

    funcionario = Funcionarios.buscar_por_cpf_original(cpf)
    
    if not funcionario or not check_password_hash(funcionario["senha"], senha):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    token = jwt.encode({
        'id': funcionario['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"token": token, "is_admin": bool(funcionario["is_admin"])}), 200


@funcionarios_bp.route("", methods=["GET"])
@token_required
def listar(current_user):
    """Todos os logados podem listar"""
    funcionarios = Funcionarios.listar_todos()
    for f in funcionarios:
        f.pop("senha", None)
    return jsonify(funcionarios), 200


@funcionarios_bp.route("/<int:id>", methods=["GET"])
@token_required
def buscar(current_user, id):
    funcionario = Funcionarios.buscar_por_id(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404
    funcionario.pop("senha", None)
    return jsonify(funcionario), 200


@funcionarios_bp.route("", methods=["POST"])
@token_required
@admin_required
def cadastrar(current_user):
    """Apenas Admin pode cadastrar"""
    data = request.json or {}
    erros = Validar.funcionario(data)
    if erros:
        return jsonify({"erros": erros}), 400

    if Funcionarios.buscar_por_cpf_original(data["cpf"]):
        return jsonify({"erro": "CPF já cadastrado"}), 409

    campos = ["nome", "rg", "cpf", "telefone", "email",
              "cargo", "endereco", "senha", "dt_criacao"]

    novo_dict = {c: data[c] for c in campos}
    novo_dict["is_admin"] = data.get("is_admin", 0) # Permite criar outro admin se quiser

    novo = Funcionarios(**novo_dict)
    novo.salvar()
    return jsonify({"mensagem": "Funcionário cadastrado com sucesso"}), 201


@funcionarios_bp.route("/<int:id>", methods=["PUT"])
@token_required
def atualizar(current_user, id):
    """Funcionário pode atualizar ele mesmo, ou Admin pode atualizar qualquer um"""
    data = request.json or {}

    if not current_user['is_admin'] and current_user['id'] != id:
        return jsonify({"erro": "Você só pode editar o próprio perfil"}), 403

    funcionario = Funcionarios.buscar_por_id(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    campos_editaveis = ["nome", "telefone", "email", "cargo", "endereco", "senha"]
    dados_para_atualizar = {c: data[c] for c in campos_editaveis if c in data}
    
    if not dados_para_atualizar:
        return jsonify({"erro": "Nenhum campo válido para atualizar"}), 400

    Funcionarios.atualizar(id, dados_para_atualizar)
    return jsonify({"mensagem": "Funcionário atualizado com sucesso"}), 200


@funcionarios_bp.route("/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def excluir(current_user, id):
    """Apenas Admin pode excluir"""
    funcionario = Funcionarios.buscar_por_id(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    Funcionarios.excluir(id)
    return jsonify({"mensagem": "Funcionário excluído com sucesso"}), 200