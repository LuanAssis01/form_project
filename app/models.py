from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db

class Usuario(UserMixin, db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefone = db.Column(db.String(20))
    cpf = db.Column(db.String(14), unique=True)
    senha_hash = db.Column(db.String(512), nullable=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    funcao = db.Column(db.String(20), default='user')

    formularios = db.relationship('Formulario', backref='usuario', lazy=True)

    def set_senha(self, senha):
        self.senha_hash = generate_password_hash(senha)

    def checar_senha(self, senha):
        return check_password_hash(self.senha_hash, senha)

class Formulario(db.Model):
    __tablename__ = 'formularios'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    dados_pessoais = db.relationship('DadosPessoais', backref='formulario', uselist=False)
    dados_sensiveis = db.relationship('DadosSensiveis', backref='formulario', uselist=False)
    dados_funcionais = db.relationship('DadosFuncionais', backref='formulario', uselist=False)
    filiacao = db.relationship('Filiacao', backref='formulario', uselist=False)
    formacao = db.relationship('DadosFormacao', backref='formulario', uselist=False)
    pos_graduacao = db.relationship('PosGraduacao', backref='formulario', uselist=False)
    mestrado = db.relationship('Mestrado', backref='formulario', uselist=False)
    doutorado = db.relationship('Doutorado', backref='formulario', uselist=False)
    dados_bancarios = db.relationship('DadosBancarios', backref='formulario', uselist=False)
    informacoes_complementares = db.relationship('InformacoesComplementares', backref='formulario', uselist=False)
    redes_sociais = db.relationship('RedeSocial', backref='formulario')
    dependentes = db.relationship('Dependente', backref='formulario')
    titulo_eleitoral = db.relationship('TituloEleitoral', backref='formulario', uselist=False)
    certidao_civil = db.relationship('CertidaoCivil', backref='formulario', uselist=False)

class DadosPessoais(db.Model):
    __tablename__ = 'dados_pessoais'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    nome = db.Column(db.String(100))
    nome_social = db.Column(db.String(100))
    data_nascimento = db.Column(db.Date)
    estado_civil = db.Column(db.String(20))
    nacionalidade = db.Column(db.String(50))
    naturalidade = db.Column(db.String(50))
    uf = db.Column(db.String(2))
    sexo = db.Column(db.String(10))

class DadosSensiveis(db.Model):
    __tablename__ = 'dados_sensiveis'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    rg = db.Column(db.String(20))
    orgao_emissor = db.Column(db.String(20))
    data_emissao = db.Column(db.Date)
    cpf = db.Column(db.String(14))
    pis_pasep = db.Column(db.String(20))
    certidao_reservista = db.Column(db.String(100))
    categoria = db.Column(db.String(50))
    serie = db.Column(db.String(50))

class DadosFuncionais(db.Model):
    __tablename__ = 'dados_funcionais'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    cargo = db.Column(db.String(100))
    matricula = db.Column(db.String(50))
    classificacao = db.Column(db.String(50))
    tipo_sanguineo = db.Column(db.String(3))
    possui_deficiencia = db.Column(db.Boolean)

class Filiacao(db.Model):
    __tablename__ = 'filiacoes'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    nome_pai = db.Column(db.String(100))
    nome_mae = db.Column(db.String(100))

class DadosFormacao(db.Model):
    __tablename__ = 'dados_formacao'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    tipo_formacao = db.Column(db.String(50))
    area = db.Column(db.String(100))

class PosGraduacao(db.Model):
    __tablename__ = 'pos_graduacoes'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    area = db.Column(db.String(100))

class Mestrado(db.Model):
    __tablename__ = 'mestrados'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    area = db.Column(db.String(100))

class Doutorado(db.Model):
    __tablename__ = 'doutorados'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    area = db.Column(db.String(100))

class DadosBancarios(db.Model):
    __tablename__ = 'dados_bancarios'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    banco = db.Column(db.String(100))
    numero_agencia = db.Column(db.String(20))
    numero_conta = db.Column(db.String(20))

class InformacoesComplementares(db.Model):
    __tablename__ = 'informacoes_complementares'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    endereco = db.Column(db.String(200))
    numero = db.Column(db.String(10))
    complemento = db.Column(db.String(50))
    bairro = db.Column(db.String(50))
    nucleo = db.Column(db.String(50))
    cidade = db.Column(db.String(100))
    uf = db.Column(db.String(2))
    cep = db.Column(db.String(10))
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(100))

class RedeSocial(db.Model):
    __tablename__ = 'redes_sociais'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    facebook = db.Column(db.String(100))
    instagram = db.Column(db.String(100))
    linkedin = db.Column(db.String(100))
    whatsapp = db.Column(db.String(100))
    telegram = db.Column(db.String(100))
    outros = db.Column(db.String(100))

class Dependente(db.Model):
    __tablename__ = 'dependentes'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    nome = db.Column(db.String(100))
    sexo = db.Column(db.String(10))
    parentesco = db.Column(db.String(50))
    cpf = db.Column(db.String(14))
    data_nascimento = db.Column(db.Date)
    possui_deficiencia = db.Column(db.Boolean)

class TituloEleitoral(db.Model):
    __tablename__ = 'titulos_eleitorais'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    numero_inscricao = db.Column(db.String(50))
    data_emissao = db.Column(db.Date)
    zona = db.Column(db.String(10))
    secao = db.Column(db.String(10))
    municipio = db.Column(db.String(100))

class CertidaoCivil(db.Model):
    __tablename__ = 'certidoes_civis'
    id = db.Column(db.Integer, primary_key=True)
    formulario_id = db.Column(db.Integer, db.ForeignKey('formularios.id'))
    tipo = db.Column(db.String(50))
    emissor = db.Column(db.String(100))
    livro = db.Column(db.String(20))
    folha = db.Column(db.String(20))
    matricula = db.Column(db.String(50))
    cartorio = db.Column(db.String(100))
    municipio = db.Column(db.String(100))
    uf = db.Column(db.String(2))
