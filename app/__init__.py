from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS
from flask_session import Session

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'uma_chave_super_secreta_aqui'
    app.config.from_object('config.Config')

    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    frontend_origin = "http://127.0.0.1:5500" # Verifique se a porta está correta
    CORS(app, supports_credentials=True, origins=[frontend_origin])

    print(f"Tentando conectar em: {app.config['SQLALCHEMY_DATABASE_URI']}")

    db.init_app(app)
    login_manager.init_app(app)

    # 🔐 Handler para APIs REST: evita redirecionamentos para rotas HTML
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'erro': 'Usuário não autenticado'}), 401

    from .models import (
        Usuario, Formulario, DadosPessoais, DadosSensiveis,
        DadosFuncionais, Filiacao, DadosFormacao, PosGraduacao,
        Mestrado, Doutorado, DadosBancarios, InformacoesComplementares,
        RedeSocial, Dependente, TituloEleitoral, CertidaoCivil
    )

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    from .routes import routes
    from .auth_routes import auth_routes
    app.register_blueprint(routes)
    app.register_blueprint(auth_routes)

    @app.route("/")
    def index():
        return "✅ API Flask conectada ao PostgreSQL com sucesso!"

    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso!")

    return app
