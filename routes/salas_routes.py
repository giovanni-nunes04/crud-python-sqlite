from flask import Blueprint, jsonify, request
from models.salas import Salas

salas_bp = Blueprint("salas", __name__, url_prefix="/api/salas")

CAMPOS_OBRIGATORIOS = ["sala", "funcionario", "data_uso", "inicio_hr", "termino_hr"]
CAMPOS_EDITAVEIS    = CAMPOS_OBRIGATORIOS


@salas_bp.route("", methods=["GET"])
def listar():
    return jsonify(Salas.listar_todas()), 200


@salas_bp.route("/opcoes", methods=["GET"])
def opcoes():
    return jsonify(Salas.SALAS_DISPONIVEIS), 200

@salas_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    sala = Salas.buscar_por_id(id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404
    return jsonify(sala), 200

@salas_bp.route("", methods=["POST"])
def cadastrar():
    data = request.json or {}

    faltando = [c for c in CAMPOS_OBRIGATORIOS if not data.get(c)]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios faltando: {faltando}"}), 400

    if data["sala"] not in Salas.SALAS_DISPONIVEIS:
        return jsonify({"erro": "Sala inválida"}), 400

    if data["termino_hr"] <= data["inicio_hr"]:
        return jsonify({"erro": "O horário de término deve ser após o início"}), 400

    if Salas.verificar_conflito(
        data["sala"], data["data_uso"],
        data["inicio_hr"], data["termino_hr"]
    ):
        return jsonify({
            "erro": (
                f"Conflito de horário! {data['sala']} já está reservada "
                f"no dia {data['data_uso']} entre {data['inicio_hr']} e {data['termino_hr']}."
            )
        }), 409

    nova = Salas(**{c: data[c] for c in CAMPOS_OBRIGATORIOS})
    nova.salvar()
    return jsonify({"mensagem": "Reserva cadastrada com sucesso"}), 201

@salas_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.json or {}

    sala_atual = Salas.buscar_por_id(id)
    if not sala_atual:
        return jsonify({"erro": "Sala não encontrada"}), 404

    atualizacao = {c: data[c] for c in CAMPOS_EDITAVEIS if c in data}
    if not atualizacao:
        return jsonify({"erro": "Nenhum campo válido para atualizar"}), 400

    sala_nome  = atualizacao.get("sala",       sala_atual["sala"])
    data_uso   = atualizacao.get("data_uso",   sala_atual["data_uso"])
    inicio_hr  = atualizacao.get("inicio_hr",  sala_atual["inicio_hr"])
    termino_hr = atualizacao.get("termino_hr", sala_atual["termino_hr"])

    if Salas.verificar_conflito(sala_nome, data_uso, inicio_hr, termino_hr, excluir_id=id):
        return jsonify({"erro": "Conflito de horário com outra reserva existente"}), 409

    Salas.atualizar(id, atualizacao)
    return jsonify({"mensagem": "Reserva atualizada com sucesso"}), 200

@salas_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    if not Salas.buscar_por_id(id):
        return jsonify({"erro": "Sala não encontrada"}), 404
    Salas.excluir(id)
    return jsonify({"mensagem": "Reserva excluída com sucesso"}), 200