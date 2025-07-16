from app import create_app, db
from app.models import *  # Importa todos os modelos

app = create_app()
with app.app_context():
    db.create_all()
    print("Tabelas criadas!")