from flask import Blueprint, jsonify, request
from models.salas import Salas
from models.funcionarios import Funcionarios
from auth import token_required

salas_bp = Blueprint("salas", __name__, url_prefix="/api/salas")


CAMPOS_OBRIGATORIOS = ["sala", "data_uso", "inicio_hr", "termino_hr"]
CAMPOS_EDITAVEIS    = ["sala", "funcionario", "data_uso", "inicio_hr", "termino_hr"]

@salas_bp.route("", methods=["GET"])
@token_required
def listar(current_user):
    return jsonify(Salas.listar_todas()), 200

@salas_bp.route("/opcoes", methods=["GET"])
@token_required
def opcoes(current_user):
    return jsonify(Salas.SALAS_DISPONIVEIS), 200

@salas_bp.route("/<int:id>", methods=["GET"])
@token_required
def buscar(current_user, id):
    sala = Salas.buscar_por_id(id)
    if not sala:
        return jsonify({"erro": "Sala não encontrada"}), 404
    return jsonify(sala), 200

@salas_bp.route("", methods=["POST"])
@token_required
def cadastrar(current_user):
    data = request.json or {}

    faltando = [c for c in CAMPOS_OBRIGATORIOS if not data.get(c)]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios faltando: {faltando}"}), 400

    if current_user.get('is_admin'):
        nome_funcionario = data.get('funcionario')
        if not nome_funcionario:
            return jsonify({"erro": "Como Admin Master, você precisa informar o nome do funcionário para a reserva."}), 400
        
        lista_funcionarios = Funcionarios.listar_todos()
        func_escolhido = next((f for f in lista_funcionarios if f['nome'] == nome_funcionario), None)
        
        if not func_escolhido:
            return jsonify({"erro": "Funcionário selecionado não encontrado no sistema."}), 404
            
        data['funcionario'] = func_escolhido['nome']
    else:
        
        data['funcionario'] = current_user['nome']

    data["criador_id"] = current_user['id']


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
                f"Conflito de horário! A {data['sala']} já está reservada "
                f"no dia {data['data_uso']} entre {data['inicio_hr']} e {data['termino_hr']}."
            )
        }), 409

    dados_nova_sala = {c: data[c] for c in CAMPOS_OBRIGATORIOS}
    dados_nova_sala["funcionario"] = data["funcionario"]
    dados_nova_sala["criador_id"]  = data["criador_id"]

    nova = Salas(**dados_nova_sala)
    nova.salvar()
    return jsonify({"mensagem": "Reserva cadastrada com sucesso"}), 201


@salas_bp.route("/<int:id>", methods=["PUT"])
@token_required
def atualizar(current_user, id):
    data = request.json or {}

    sala_atual = Salas.buscar_por_id(id)
    if not sala_atual:
        return jsonify({"erro": "Sala não encontrada"}), 404

    if sala_atual['criador_id'] != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"erro": "Acesso negado. Você só pode editar as reservas que você criou."}), 403

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
@token_required
def excluir(current_user, id):
    sala_atual = Salas.buscar_por_id(id)
    if not sala_atual:
        return jsonify({"erro": "Sala não encontrada"}), 404

    if sala_atual['criador_id'] != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"erro": "Acesso negado. Você só pode excluir as reservas que você criou."}), 403

    Salas.excluir(id)
    return jsonify({"mensagem": "Reserva excluída com sucesso"}), 200