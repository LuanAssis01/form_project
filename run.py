from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.route("/")
    def index():
        return "✅ API Flask conectada ao PostgreSQL com sucesso!"

    with app.app_context():
        db.create_all()  # cria tabelas automaticamente

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
