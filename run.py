from app import create_app, db
from app.models import *

app = create_app()

@app.cli.command('create-tables')
def create_tables():
    with app.app_context():
        db.create_all()
        print("Tabelas criadas com sucesso!")

if __name__ == '__main__':
    app.run(debug=True)