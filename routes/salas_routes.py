from flask import Blueprint, jsonify, request
from models.salas import Salas
from validator import Validar

salas_bp = Blueprint("salas", __name__, url_prefix="/api/salas")


# 🔵 LISTAR TODAS AS SALAS
@salas_bp.route("", methods=["GET"])
def listar():
    salas = Salas.listar_todos()
    return jsonify(salas), 200


# 🔵 BUSCAR SALA POR ID
@salas_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    sala = Salas.buscar_por_id(id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404

    return jsonify(sala), 200


# 🔵 CADASTRAR NOVA SALA
@salas_bp.route("", methods=["POST"])
def cadastrar():
    data = request.json or {}

    # (opcional) validação — se você tiver no validator
    # erros = Validar.sala(data)
    # if erros:
    #     return jsonify({"erros": erros}), 400

    campos = ["sala", "funcionario", "status", "data_uso", "inicio_hr", "termino_hr"]

    nova = Salas(**{c: data.get(c) for c in campos})
    nova.salvar()

    return jsonify({"mensagem": "Sala cadastrada com sucesso"}), 201


# 🔵 ATUALIZAR SALA
@salas_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.json or {}

    sala = Salas.buscar_por_id(id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404

    campos_editaveis = ["sala", "funcionario", "status", "data_uso", "inicio_hr", "termino_hr"]

    dados_para_atualizar = {c: data[c] for c in campos_editaveis if c in data}

    if not dados_para_atualizar:
        return jsonify({"erro": "Nenhum campo válido para atualizar"}), 400

    Salas.atualizar(id, dados_para_atualizar)

    return jsonify({"mensagem": "Sala atualizada com sucesso"}), 200


# 🔴 EXCLUIR SALA
@salas_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    sala = Salas.buscar_por_id(id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404

    Salas.excluir(id)

    return jsonify({"mensagem": "Sala excluída com sucesso"}), 200