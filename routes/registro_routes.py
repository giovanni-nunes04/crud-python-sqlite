from flask import Blueprint, jsonify, request
from models.registro import Registro
from validator import Validar

registros_bp = Blueprint("registros", __name__, url_prefix="/api/registros")


@registros_bp.route("", methods=["GET"])
def listar():
    registros = Registro.listar_todos()
    return jsonify(registros), 200


@registros_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    registro = Registro.buscar_por_id(id)
    if not registro:
        return jsonify({"erro": "Registro não encontrado"}), 404
    return jsonify(registro), 200

@registros_bp.route("", methods=["POST"])
def cadastrar():
    data = request.json or {}

    erros = Validar.registro(data)
    if erros:
        return jsonify({"erros": erros}), 400

    if Registro.buscar_por_id(data["id"]):
        return jsonify({"erro": "Usuário já cadastrado"}), 409

    campos = ["usuario", "senha", "data_acesso"]

    novo = Registro(**{c: data[c] for c in campos})
    novo.salvar()
    return jsonify({"mensagem": "Registro cadastrado com sucesso"}), 201


@registros_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.json or {}

    registro = Registro.buscar_por_id(id)
    if not registro:
        return jsonify({"erro": "Registro não encontrado"}), 404

    campos_editaveis = ["usuario", "senha", "data_acesso"]
    erros = []

    validadores = {
        "usuario":  Validar.usuario,
        "senha":    Validar.senha,
        "data_acesso": Validar.data_acesso,
    }

    for campo in campos_editaveis:
        if campo in data:
            if not validadores[campo](data[campo]):
                erros.append(f"Campo '{campo}' inválido.")

    if erros:
        return jsonify({"erros": erros}), 400

    dados_para_atualizar = {c: data[c] for c in campos_editaveis if c in data}
    if not dados_para_atualizar:
        return jsonify({"erro": "Nenhum campo válido para atualizar"}), 400

    Registro.atualizar(id, dados_para_atualizar)
    return jsonify({"mensagem": "Registro atualizado com sucesso"}), 200


@registros_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    registro = Registro.buscar_por_id(id)
    if not registro:
        return jsonify({"erro": "Registro não encontrado"}), 404

    Registro.excluir(id)
    return jsonify({"mensagem": "Registro excluído com sucesso"}), 200