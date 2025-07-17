from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, Usuario

auth_routes = Blueprint('auth', __name__, url_prefix='/auth')

@auth_routes.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados = request.get_json()
    nome_completo = dados.get('nome')
    email = dados.get('email')
    telefone = dados.get('telefone')
    cpf = dados.get('cpf')
    senha = dados.get('senha')
    
    if not nome_completo:
        return jsonify({'erro': 'O campo nome é obrigatório'}), 400
    
    if Usuario.query.filter((Usuario.email == email) | (Usuario.cpf == cpf)).first():
        return jsonify({'erro': 'Usuário com esse email ou CPF já existe'}), 400

    novo_usuario = Usuario(
        nome_completo=nome_completo,
        email=email,
        telefone=telefone,
        cpf=cpf
    )
    novo_usuario.set_senha(senha)

    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário cadastrado com sucesso'}), 201

@auth_routes.route('/login', methods=['POST'])
def login():
    dados = request.get_json()
    email = dados.get('email')
    senha = dados.get('senha')

    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and usuario.checar_senha(senha):
        login_user(usuario)
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200
    return jsonify({'erro': 'Credenciais inválidas'}), 401

@auth_routes.route('/logout', methods=['POST'])
@login_required
def logout():
    print("Tentando fazer logout - usuário atual:", current_user.is_authenticated)
    if not current_user.is_authenticated:
        print("Nenhum usuário autenticado para fazer logout!")
        return jsonify({'erro': 'Nenhum usuário autenticado'}), 401
    
    logout_user()
    print("Logout realizado com sucesso")
    return jsonify({'mensagem': 'Logout realizado com sucesso'}), 200

@auth_routes.route('/usuario', methods=['GET'])
@login_required
def usuario_logado():
    try:
        return jsonify({
            'id': current_user.id,
            'nome': current_user.nome_completo,
            'email': current_user.email
        }), 200
    except Exception as e:
        return jsonify({'erro': 'Erro interno na busca por usuário logado'}), 500

    