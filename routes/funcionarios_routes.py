from flask import Blueprint, jsonify, request
from models.funcionarios import Funcionarios
from validator import Validar

funcionarios_bp = Blueprint("funcionarios", __name__, url_prefix="/api/funcionarios")


@funcionarios_bp.route("", methods=["GET"])
def listar():
    funcionarios = Funcionarios.listar_todos()
    for f in funcionarios:
        f.pop("senha", None)
    return jsonify(funcionarios), 200


@funcionarios_bp.route("/<int:id>", methods=["GET"])
def buscar(id):
    funcionario = Funcionarios.buscar_por_id(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404
    funcionario.pop("senha", None)
    return jsonify(funcionario), 200

@funcionarios_bp.route("", methods=["POST"])
def cadastrar():
    data = request.json or {}

    erros = Validar.funcionario(data)
    if erros:
        return jsonify({"erros": erros}), 400

    if Funcionarios.buscar_por_cpf(data["cpf"]):
        return jsonify({"erro": "CPF já cadastrado"}), 409

    campos = ["nome", "rg", "cpf", "telefone", "email",
              "cargo", "endereco", "senha", "dt_criacao"]

    novo = Funcionarios(**{c: data[c] for c in campos})
    novo.salvar()
    return jsonify({"mensagem": "Funcionário cadastrado com sucesso"}), 201


@funcionarios_bp.route("/<int:id>", methods=["PUT"])
def atualizar(id):
    data = request.json or {}

    funcionario = Funcionarios.buscar_por_id(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    campos_editaveis = ["nome", "telefone", "email", "cargo", "endereco", "senha"]
    erros = []

    validadores = {
        "nome":     Validar.nome,
        "telefone": Validar.telefone,
        "email":    Validar.email,
        "cargo":    Validar.cargo,
        "endereco": Validar.endereco,
        "senha":    Validar.senha,
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

    Funcionarios.atualizar(id, dados_para_atualizar)
    return jsonify({"mensagem": "Funcionário atualizado com sucesso"}), 200


@funcionarios_bp.route("/<int:id>", methods=["DELETE"])
def excluir(id):
    funcionario = Funcionarios.buscar_por_id(id)
    if not funcionario:
        return jsonify({"erro": "Funcionário não encontrado"}), 404

    Funcionarios.excluir(id)
    return jsonify({"mensagem": "Funcionário excluído com sucesso"}), 200