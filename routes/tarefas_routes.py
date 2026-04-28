from flask import Blueprint, jsonify, request
from models.tarefas import Tarefas
from validator import Validar

tarefas_bp = Blueprint("tarefas", __name__, url_prefix="/api/tarefas")


@tarefas_bp.route("", methods=["GET"])
def listar():
    return jsonify(Tarefas.listar_todas()), 200


@tarefas_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    tarefa = Tarefas.buscar_por_id(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404
    return jsonify(tarefa), 200

@tarefas_bp.route("", methods=["POST"])
def cadastrar():
    data = request.json or {}

    erros = Validar.tarefa(data)
    if erros:
        return jsonify({"erros": erros}), 400

    campos = ["funcionario", "funcao", "local", "tarefa", "prioridade",
              "status", "inicio_dt", "termino_dt", "responsavel_registro",
              "dt_criacao"]

    nova = Tarefas(**{c: data[c] for c in campos})
    nova.salvar()
    return jsonify({"mensagem": "Tarefa cadastrada com sucesso"}), 201


@tarefas_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.json or {}

    novo_status = data.get("status", "")
    if not Validar.status_tarefa(novo_status):
        return jsonify({
            "erro": "Campo 'status' deve ser: pendente, em andamento, concluida ou cancelada."
        }), 400

    tarefa = Tarefas.buscar_por_id(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    Tarefas.atualizar_status(id, novo_status)
    return jsonify({"mensagem": "Status atualizado com sucesso"}), 200


@tarefas_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    tarefa = Tarefas.buscar_por_id(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    Tarefas.excluir(id)
    return jsonify({"mensagem": "Tarefa excluída com sucesso"}), 200
