import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Dados de conexão com o Postgres
    POSTGRES_USER = os.getenv('POSTGRES_USER', 'admin')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin123')
    POSTGRES_DB = os.getenv('POSTGRES_DB', 'smsi_db')
    POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

    SQLALCHEMY_DATABASE_URI = (
        f'postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}'
        f'@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Chave secreta da aplicação
    SECRET_KEY = os.getenv('SECRET_KEY', 'uma_chave_super_secreta_aqui')
    
    SESSION_COOKIE_SAMESITE  = 'None'   # permite envio de cookie em requisições cross‑site
    SESSION_COOKIE_SECURE    = False  
    SESSION_COOKIE_NAME = "session"     # Apenas True se usar HTTPS

    REMEMBER_COOKIE_SAMESITE = 'None'
    REMEMBER_COOKIE_SECURE   = False
