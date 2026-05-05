from flask import Blueprint, jsonify, request
from models.tarefas import Tarefas
from models.funcionarios import Funcionarios # Importante para buscar os cargos
from auth import token_required
import datetime

tarefas_bp = Blueprint("tarefas", __name__, url_prefix="/api/tarefas")

@tarefas_bp.route("", methods=["GET"])
@token_required
def listar(current_user):
    # Retorna a lista de tarefas para montar o Dashboard
    return jsonify(Tarefas.listar_todas()), 200

@tarefas_bp.route("", methods=["POST"])
@token_required
def cadastrar(current_user):
    data = request.json or {}
    
    # 1. Dados automáticos de segurança e rastreio
    data['criador_id'] = current_user['id']
    data['responsavel_registro'] = current_user['nome']
    
    # Garante que temos a data de criação
    if 'dt_criacao' not in data or not data['dt_criacao']:
        data['dt_criacao'] = datetime.date.today().strftime("%Y-%m-%d")

    # 2. Regra de Negócio: Funcionário vs Admin Master
    if current_user.get('is_admin'):
        # Se for Admin, ele deve ter enviado o nome do funcionário escolhido
        nome_funcionario = data.get('funcionario')
        if not nome_funcionario:
            return jsonify({"erro": "Como Admin, você precisa informar o nome do funcionário."}), 400
        
        # Busca a lista de funcionários para pegar a função (cargo) do escolhido
        lista_funcionarios = Funcionarios.listar_todos()
        func_escolhido = next((f for f in lista_funcionarios if f['nome'] == nome_funcionario), None)
        
        if not func_escolhido:
            return jsonify({"erro": "Funcionário selecionado não encontrado no sistema."}), 404
            
        data['funcionario'] = func_escolhido['nome']
        data['funcao'] = func_escolhido['cargo']
        
    else:
        # Se for funcionário comum, forçamos os dados dele (ignora o que veio no formulário)
        data['funcionario'] = current_user['nome']
        data['funcao'] = current_user['cargo']

    # 3. Salva no banco de dados
    try:
        Tarefas.salvar(data)
        return jsonify({"mensagem": "Tarefa cadastrada com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": f"Erro ao salvar tarefa: {str(e)}"}), 500

@tarefas_bp.route("/<int:id>", methods=["PUT"])
@token_required
def atualizar(current_user, id):
    data = request.json or {}
    tarefa = Tarefas.buscar_por_id(id)
    
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    # Regra: Só pode atualizar se for o dono da tarefa ou Admin Master
    if tarefa['criador_id'] != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"erro": "Você não tem permissão para editar uma tarefa que não criou."}), 403

    # Vamos permitir atualizar apenas o status (você pode adicionar mais campos se quiser)
    dados_para_atualizar = {}
    if 'status' in data:
        dados_para_atualizar['status'] = data['status']
        
    Tarefas.atualizar(id, dados_para_atualizar)
    return jsonify({"mensagem": "Tarefa atualizada com sucesso"}), 200

@tarefas_bp.route("/<int:id>", methods=["DELETE"])
@token_required
def excluir(current_user, id):
    tarefa = Tarefas.buscar_por_id(id)
    if not tarefa:
        return jsonify({"erro": "Tarefa não encontrada"}), 404

    # Regra: Só exclui se for o dono (ou Admin Master)
    if tarefa['criador_id'] != current_user['id'] and not current_user.get('is_admin'):
        return jsonify({"erro": "Você não tem permissão para excluir uma tarefa que não criou."}), 403

    Tarefas.excluir(id)
    return jsonify({"mensagem": "Tarefa excluída com sucesso"}), 200