import jwt
import os
from functools import wraps
from flask import request, jsonify
from models.funcionarios import Funcionarios
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("Nenhuma SECRET_KEY encontrada. Verifique seu arquivo .env!")

def token_required(f):
    """Garante que o usuário está logado (Admin ou Funcionário)"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]

        if not token:
            return jsonify({'erro': 'Token de acesso ausente! Faça login.'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = Funcionarios.buscar_por_id(data['id'])
            if not current_user:
                return jsonify({'erro': 'Usuário não encontrado!'}), 401
        except:
            return jsonify({'erro': 'Token inválido ou expirado!'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    """Garante que APENAS o Admin Master pode acessar"""
    @wraps(f)
    def decorated(current_user, *args, **kwargs):
        if not current_user.get('is_admin'):
            return jsonify({'erro': 'Acesso negado. Requer privilégios de Admin Master.'}), 403
        return f(current_user, *args, **kwargs)
    return decorated