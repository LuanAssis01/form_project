from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
# Importando todos os models necessários
from app.models import (
    db, Formulario, DadosPessoais, DadosSensiveis, DadosFuncionais, 
    Filiacao, DadosFormacao, PosGraduacao, Mestrado, Doutorado, DadosBancarios, 
    InformacoesComplementares, RedeSocial, Dependente, TituloEleitoral, CertidaoCivil
)
import traceback

routes = Blueprint('routes', __name__)

def extrair_dados(dados, modelo_classe, campos):
    """Cria uma instância de um modelo a partir de um dicionário de dados."""
    if not dados:
        return None
    instancia = modelo_classe()
    for campo in campos:
        # Usamos .get() para não dar erro se a chave não existir no JSON
        valor = dados.get(campo)
        if valor is not None:
            setattr(instancia, campo, valor)
    return instancia

def serializar_formulario(f):
    """Converte um objeto Formulario completo em um dicionário para resposta JSON."""
    def to_dict(obj, campos):
        if not obj: return None
        return {campo: getattr(obj, campo, None) for campo in campos}

    def list_to_dict(lista_obj, campos):
        if not lista_obj: return []
        return [to_dict(item, campos) for item in lista_obj]

    return {
        'id': f.id,
        'usuario_id': f.usuario_id,
        'dados_pessoais': to_dict(f.dados_pessoais, ['nome', 'nome_social', 'data_nascimento', 'estado_civil', 'nacionalidade', 'naturalidade', 'uf', 'sexo']),
        'dados_sensiveis': to_dict(f.dados_sensiveis, ['rg', 'orgao_emissor', 'data_emissao', 'cpf', 'pis_pasep', 'certidao_reservista', 'categoria', 'serie']),
        'dados_funcionais': to_dict(f.dados_funcionais, ['cargo', 'matricula', 'classificacao', 'tipo_sanguineo', 'possui_deficiencia']),
        'filiacao': to_dict(f.filiacao, ['nome_pai', 'nome_mae']),
        'formacao': to_dict(f.formacao, ['tipo_formacao', 'area']),
        'pos_graduacao': to_dict(f.pos_graduacao, ['area']),
        'mestrado': to_dict(f.mestrado, ['area']),
        'doutorado': to_dict(f.doutorado, ['area']),
        'dados_bancarios': to_dict(f.dados_bancarios, ['banco', 'numero_agencia', 'numero_conta']),
        'informacoes_complementares': to_dict(f.informacoes_complementares, ['endereco', 'numero', 'complemento', 'bairro', 'nucleo', 'cidade', 'uf', 'cep', 'telefone', 'email']),
        'titulo_eleitoral': to_dict(f.titulo_eleitoral, ['numero_inscricao', 'data_emissao', 'zona', 'secao', 'municipio']),
        'certidao_civil': to_dict(f.certidao_civil, ['tipo', 'emissor', 'livro', 'folha', 'matricula', 'cartorio', 'municipio', 'uf']),
        'redes_sociais': list_to_dict(f.redes_sociais, ['facebook', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'outros']),
        'dependentes': list_to_dict(f.dependentes, ['nome', 'sexo', 'parentesco', 'cpf', 'data_nascimento', 'possui_deficiencia']),
    }

# --- ROTAS CRUD ---

@routes.route('/servidores', methods=['POST'])
@login_required
def criar_ficha():
    dados = request.get_json()
    if not dados:
        return jsonify({'erro': 'Requisição sem dados JSON'}), 400

    try:
        nova_ficha = Formulario(usuario_id=current_user.id)

        # Relacionamentos 1-para-1
        nova_ficha.dados_pessoais = extrair_dados(dados.get('dados_pessoais'), DadosPessoais, ['nome', 'nome_social', 'data_nascimento', 'estado_civil', 'nacionalidade', 'naturalidade', 'uf', 'sexo'])
        nova_ficha.dados_sensiveis = extrair_dados(dados.get('dados_sensiveis'), DadosSensiveis, ['rg', 'orgao_emissor', 'data_emissao', 'cpf', 'pis_pasep', 'certidao_reservista', 'categoria', 'serie'])
        nova_ficha.dados_funcionais = extrair_dados(dados.get('dados_funcionais'), DadosFuncionais, ['cargo', 'matricula', 'classificacao', 'tipo_sanguineo', 'possui_deficiencia'])
        nova_ficha.filiacao = extrair_dados(dados.get('filiacao'), Filiacao, ['nome_pai', 'nome_mae'])
        nova_ficha.formacao = extrair_dados(dados.get('formacao'), DadosFormacao, ['tipo_formacao', 'area'])
        nova_ficha.pos_graduacao = extrair_dados(dados.get('pos_graduacao'), PosGraduacao, ['area'])
        nova_ficha.mestrado = extrair_dados(dados.get('mestrado'), Mestrado, ['area'])
        nova_ficha.doutorado = extrair_dados(dados.get('doutorado'), Doutorado, ['area'])
        nova_ficha.dados_bancarios = extrair_dados(dados.get('dados_bancarios'), DadosBancarios, ['banco', 'numero_agencia', 'numero_conta'])
        nova_ficha.informacoes_complementares = extrair_dados(dados.get('informacoes_complementares'), InformacoesComplementares, ['endereco', 'numero', 'complemento', 'bairro', 'nucleo', 'cidade', 'uf', 'cep', 'telefone', 'email'])
        nova_ficha.titulo_eleitoral = extrair_dados(dados.get('titulo_eleitoral'), TituloEleitoral, ['numero_inscricao', 'data_emissao', 'zona', 'secao', 'municipio'])
        nova_ficha.certidao_civil = extrair_dados(dados.get('certidao_civil'), CertidaoCivil, ['tipo', 'emissor', 'livro', 'folha', 'matricula', 'cartorio', 'municipio', 'uf'])

        # Relacionamentos 1-para-N (Listas)
        if dados.get('dependentes'):
            for dep_data in dados['dependentes']:
                dependente = extrair_dados(dep_data, Dependente, ['nome', 'sexo', 'parentesco', 'cpf', 'data_nascimento', 'possui_deficiencia'])
                if dependente: nova_ficha.dependentes.append(dependente)
        
        if dados.get('redes_sociais'):
            for rede_data in dados['redes_sociais']:
                rede = extrair_dados(rede_data, RedeSocial, ['facebook', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'outros'])
                if rede: nova_ficha.redes_sociais.append(rede)

        db.session.add(nova_ficha)
        db.session.commit()

        return jsonify({'mensagem': 'Ficha criada com sucesso', 'id': nova_ficha.id}), 201

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'erro': 'Ocorreu um erro interno ao criar a ficha', 'detalhes': str(e)}), 500


@routes.route('/servidores', methods=['GET'])
@login_required
def listar_fichas():
    # Retorna uma lista resumida para melhor performance.
    fichas = db.session.query(
        Formulario.id,
        DadosPessoais.nome,
        DadosSensiveis.cpf,
        DadosFuncionais.cargo
    ).join(DadosPessoais, Formulario.id == DadosPessoais.formulario_id, isouter=True)\
     .join(DadosSensiveis, Formulario.id == DadosSensiveis.formulario_id, isouter=True)\
     .join(DadosFuncionais, Formulario.id == DadosFuncionais.formulario_id, isouter=True)\
     .filter(Formulario.usuario_id == current_user.id).all()

    resultado = [{'id': f.id, 'nome': f.nome, 'cpf': f.cpf, 'cargo': f.cargo} for f in fichas]
    return jsonify(resultado), 200


@routes.route('/servidores/<int:id>', methods=['GET'])
@login_required
def buscar_ficha(id):
    ficha = Formulario.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    return jsonify(serializar_formulario(ficha)), 200


@routes.route('/servidores/<int:id>', methods=['PUT'])
@login_required
def atualizar_ficha(id):
    ficha = Formulario.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    dados = request.get_json()

    try:
        # Lógica de atualização genérica para relacionamentos 1-para-1
        def atualizar_sub_modelo(sub_modelo_nome, modelo_classe):
            if sub_modelo_nome in dados:
                sub_dados = dados.get(sub_modelo_nome)
                if not sub_dados: return
                
                instancia_existente = getattr(ficha, sub_modelo_nome)
                if not instancia_existente:
                    instancia_existente = modelo_classe()
                    setattr(ficha, sub_modelo_nome, instancia_existente)

                for campo, valor in sub_dados.items():
                    if hasattr(instancia_existente, campo):
                        setattr(instancia_existente, campo, valor)
        
        # Atualiza todos os sub-modelos 1-para-1
        atualizar_sub_modelo('dados_pessoais', DadosPessoais)
        atualizar_sub_modelo('dados_sensiveis', DadosSensiveis)
        atualizar_sub_modelo('dados_funcionais', DadosFuncionais)
        # ... adicione todos os outros aqui ...
        atualizar_sub_modelo('filiacao', Filiacao)
        atualizar_sub_modelo('formacao', DadosFormacao)
        atualizar_sub_modelo('pos_graduacao', PosGraduacao)
        atualizar_sub_modelo('mestrado', Mestrado)
        atualizar_sub_modelo('doutorado', Doutorado)
        atualizar_sub_modelo('dados_bancarios', DadosBancarios)
        atualizar_sub_modelo('informacoes_complementares', InformacoesComplementares)
        atualizar_sub_modelo('titulo_eleitoral', TituloEleitoral)
        atualizar_sub_modelo('certidao_civil', CertidaoCivil)


        # Lógica de atualização para relacionamentos 1-para-N (apaga e recria)
        if 'dependentes' in dados:
            [db.session.delete(d) for d in ficha.dependentes] # Apaga antigos
            if dados['dependentes']:
                for dep_data in dados['dependentes']: # Cria novos
                    dependente = extrair_dados(dep_data, Dependente, ['nome', 'sexo', 'parentesco', 'cpf', 'data_nascimento', 'possui_deficiencia'])
                    if dependente: ficha.dependentes.append(dependente)

        if 'redes_sociais' in dados:
            [db.session.delete(r) for r in ficha.redes_sociais] # Apaga antigos
            if dados['redes_sociais']:
                for rede_data in dados['redes_sociais']: # Cria novos
                    rede = extrair_dados(rede_data, RedeSocial, ['facebook', 'instagram', 'linkedin', 'whatsapp', 'telegram', 'outros'])
                    if rede: ficha.redes_sociais.append(rede)

        db.session.commit()
        return jsonify({'mensagem': 'Ficha atualizada com sucesso'}), 200

    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'erro': 'Ocorreu um erro interno ao atualizar a ficha', 'detalhes': str(e)}), 500


@routes.route('/servidores/<int:id>', methods=['DELETE'])
@login_required
def deletar_ficha(id):
    # Lembre-se que isso depende da configuração 'cascade' nos models!
    ficha = Formulario.query.filter_by(id=id, usuario_id=current_user.id).first_or_404()
    
    try:
        db.session.delete(ficha)
        db.session.commit()
        return jsonify({'mensagem': 'Ficha excluída com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        traceback.print_exc()
        return jsonify({'erro': 'Ocorreu um erro interno ao excluir a ficha', 'detalhes': str(e)}), 500