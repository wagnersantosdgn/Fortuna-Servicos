import os # Permite interagir com o sistema operacional, como acessar variáveis de ambiente
import re # Permite trabalhar com expressões regulares, úteis para validação e formatação de strings
from flask import Flask, request, jsonify # Permite criar a aplicação web, lidar com requisições HTTP e retornar respostas em formato JSON
import mysql.connector # Permite conectar e interagir com um banco de dados MySQL
from dotenv import load_dotenv # Permite carregar variáveis de ambiente de um arquivo .env
from flask_cors import CORS # Permite lidar com requisições de diferentes origens (Cross-Origin Resource Sharing)
from datetime import datetime # Permite trabalhar com datas e horas

load_dotenv() # Carrega as variáveis de ambiente do arquivo .env

app = Flask(__name__) # Cria a aplicação Flask

CORS(app, resources={r"/api/*": {"origins":  "*", "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"]}}) # Configura o CORS para permitir requisições de qualquer origem para rotas que começam com /api/

db_config = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS'),
    'port': int(os.getenv('DB_PORT'))
} # Configura os parâmetros de conexão com o banco de dados MySQL, obtendo os valores das variáveis de ambiente carregadas do arquivo .env

def get_db_connection():
    return mysql.connector.connect(**db_config) # Função que cria e retorna uma conexão com o banco de dados MySQL usando os parâmetros definidos em db_config

# Valida e formata telefones brasileiros para armazenamento e uso em APIs (ex: WhatsApp):
# - Garante +55 como DDI padrão
# - Exige DDD (2 dígitos) e número móvel com 9 como primeiro dígito
# - Aceita entradas como '(31) 98842-3005', '31988423005', '+55 31 98842-3005'
# Retorna (e164, display) onde e164 é '+55DDDNXXXXXXXX' (sem espaços) e display é '+55 DD NNNNN-NNNN'

def validate_and_format_phone(phone_str):
    if not phone_str:
        raise ValueError('Telefone é obrigatório.')
    # Extrai apenas dígitos
    digits = re.sub(r'\D', '', phone_str)
    digits = digits.lstrip('0')
    # Remove código do país se presente
    if digits.startswith('55'):
        core = digits[2:]
    else:
        core = digits
    # Se faltar o 9 (número com 8 dígitos após o DDD), insere o 9 como padrão
    if len(core) == 10:
        core = core[:2] + '9' + core[2:]
    if len(core) != 11:
        raise ValueError('Telefone inválido. Informe DDD + número (ex: (31) 98842-3005).')
    # Verifica se é número móvel começando com 9
    if core[2] != '9':
        raise ValueError('Número móvel inválido: deve começar com 9 (ex: 98842-3005).')
    e164 = '55' + core
    display = f'55 {core[:2]} {core[2:7]}-{core[7:]}'
    return e164, display


# Valida e formata CPF (validação completa com dígitos verificadores):
# - Rejeita sequências repetidas (ex: 00000000000)
# - Rejeita CPF inválido como 000.000.000-00
# - Retorna (digits, display) onde digits é apenas os 11 dígitos e display é formatado '000.000.000-00'

def validate_and_format_cpf(cpf_str):
    if not cpf_str:
        raise ValueError('CPF é obrigatório.')
    digits = re.sub(r'\D', '', cpf_str)
    if len(digits) != 11:
        raise ValueError('CPF inválido: deve conter 11 dígitos.')
    # Rejeita sequências repetidas como '00000000000', '11111111111', ...
    if digits == digits[0] * 11:
        raise ValueError('CPF inválido.')
    # Cálculo dos dígitos verificadores
    def calc_digit(digs):
        s = 0
        for i, multiplier in enumerate(range(len(digs)+1, 1, -1)):
            s += int(digs[i]) * multiplier
        r = s % 11
        return '0' if r < 2 else str(11 - r)
    first_check = calc_digit(digits[:9])
    second_check = calc_digit(digits[:9] + first_check)
    if digits[9] != first_check or digits[10] != second_check:
        raise ValueError('CPF inválido.')
    display = f'{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}'
    return digits, display


class Usuarios:
    def __init__(self, nome, email, cpf, senha, telefone, endereco_usuario, aceitou_lgpd, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.telefone = telefone
        self.endereco_usuario = endereco_usuario
        self.aceitou_lgpd = aceitou_lgpd
        self.data_consentimento = datetime.now()
        
class Prestadores:
    def __init__(self, nome, email, cpf, senha, telefone, endereco_prestador, categoria_servico, descricao, aceitou_lgpd, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.senha = senha
        self.telefone = telefone
        self.endereco_prestador = endereco_prestador
        self.categoria_servico = categoria_servico
        self.descricao = descricao
        self.aceitou_lgpd = aceitou_lgpd
        self.data_consentimento = datetime.now()
        
class Pedidos:
    def __init__(self, usuario_id, prestador_id, descricao_servico, valor, data_agendamento, status, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.prestador_id = prestador_id
        self.descricao_servico = descricao_servico
        self.valor = valor
        self.data_agendamento = data_agendamento
        self.status = status
        self.data_pedido = datetime.now()
class Avaliacoes:
    def __init__(self, pedido_id, usuario_id, prestador_id, nota, comentario, id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.usuario_id = usuario_id
        self.prestador_id = prestador_id
        self.nota = nota
        self.comentario = comentario
        self.data_avaliacao = datetime.now()
        
@app.route('/api/usuario', methods=['POST'])
def cadastrar_usuario():
    conn = None
    try:
        dados = request.get_json()
        try:
            telefone_e164, telefone_display = validate_and_format_phone(dados.get('telefone', ''))
            cpf_digits, cpf_display = validate_and_format_cpf(dados.get('cpf', ''))
        except ValueError as ve:
            return jsonify({"erro": str(ve)}), 400
        usuario = Usuarios(dados['nome'], dados['email'], cpf_display, dados['senha'], telefone_e164, dados['endereco_usuario'], dados['aceitou_lgpd'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nome, email, cpf, senha, telefone, endereco_usuario, aceitou_lgpd, data_consentimento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, validate_and_format_cpf(dados.get('cpf', ''))[1], usuario.senha, usuario.telefone, usuario.endereco_usuario, usuario.aceitou_lgpd, usuario.data_consentimento))
        conn.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/usuario/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    conn = None
    try:
        dados = request.get_json()
        try:
            telefone_e164, telefone_display = validate_and_format_phone(dados.get('telefone', ''))
            cpf_digits, cpf_display = validate_and_format_cpf(dados.get('cpf', ''))
        except ValueError as ve:
            return jsonify({"erro": str(ve)}), 400
        usuario = Usuarios(dados['nome'], dados['email'], cpf_display, dados['senha'], telefone_e164, dados['endereco_usuario'], dados['aceitou_lgpd'], dados.get('data_consentimento'))
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE usuarios SET nome=%s, email=%s, cpf=%s, senha=%s, telefone=%s, endereco_usuario=%s, aceitou_lgpd=%s, data_consentimento=%s WHERE id=%s"""
        cursor.execute(sql, (usuario.nome, usuario.email, validate_and_format_cpf(dados.get('cpf', ''))[1], usuario.senha, usuario.telefone, usuario.endereco_usuario, usuario.aceitou_lgpd, usuario.data_consentimento, id))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Usuário não encontrado."}), 404
        return jsonify({"message": "Os dados foram atualizados!"}), 200
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/usuario/<int:id>', methods=['DELETE'])
def excluir_usuario(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Usuário não encontrado."}), 404
        return jsonify({"message": "Usuário excluído com sucesso!"}), 200
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/prestador', methods=['POST'])
def cadastrar_prestador():
    conn = None
    try:
        dados = request.get_json()
        try:
            telefone_e164, telefone_display = validate_and_format_phone(dados.get('telefone', ''))
        except ValueError as ve:
            return jsonify({"erro": str(ve)}), 400
        prestador = Prestadores(dados['nome'], dados['email'], dados['cpf'], dados['senha'], telefone_e164, dados['endereco_prestador'], dados['categoria_servico'], dados['descricao'], dados['aceitou_lgpd'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO prestadores (nome, email, cpf, senha, telefone, endereco_prestador, categoria_servico, descricao, aceitou_lgpd, data_consentimento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (prestador.nome, prestador.email, validate_and_format_cpf(dados.get('cpf', ''))[1], prestador.senha, prestador.telefone, prestador.endereco_prestador, prestador.categoria_servico, prestador.descricao, prestador.aceitou_lgpd, prestador.data_consentimento))
        conn.commit()
        return jsonify({"message": "Prestador cadastrado com sucesso!"}), 201
    except ValueError as ve:
        if conn: conn.rollback()
        return jsonify({"erro": str(ve)}), 400
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/prestador/<int:id>', methods=['PUT'])
def atualizar_prestador(id):
    conn = None
    try:
        dados = request.get_json()
        try:
            telefone_e164, telefone_display = validate_and_format_phone(dados.get('telefone', ''))
        except ValueError as ve:
            return jsonify({"erro": str(ve)}), 400
        prestador = Prestadores(dados['nome'], dados['email'], dados['cpf'], dados['senha'], telefone_e164, dados['endereco_prestador'], dados['categoria_servico'], dados['descricao'], dados['aceitou_lgpd'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE prestadores SET nome=%s, email=%s, cpf=%s, senha=%s, telefone=%s, endereco_prestador=%s, categoria_servico=%s, descricao=%s, aceitou_lgpd=%s, data_consentimento=%s WHERE id=%s"""
        cursor.execute(sql, (prestador.nome, prestador.email, validate_and_format_cpf(dados.get('cpf', ''))[1], prestador.senha, prestador.telefone, prestador.endereco_prestador, prestador.categoria_servico, prestador.descricao, prestador.aceitou_lgpd, prestador.data_consentimento, id))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Prestador não encontrado."}), 404
        return jsonify({"message": "Os dados foram atualizados!"}), 200
    except ValueError as ve:
        if conn: conn.rollback()
        return jsonify({"erro": str(ve)}), 400
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/prestador/<int:id>', methods=['DELETE'])
def excluir_prestador(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM prestadores WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Prestador não encontrado."}), 404
        return jsonify({"message": "Prestador excluído!"}), 200
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/prestador/buscar', methods=['GET'])
def buscar_prestadores():
    conn = None
    try:
        nome = request.args.get('nome')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        sql = "SELECT * FROM prestadores WHERE 1=1"
        params = []
        if nome:
            sql += " AND nome LIKE %s"
            params.append(f"%{nome}%") #
        cursor.execute(sql, tuple(params))
        prestadores = cursor.fetchall()
        return jsonify(prestadores), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/pedidos', methods=['POST'])
def cadastrar_pedido():
    conn = None
    try:
        dados = request.get_json()
        pedido = Pedidos(dados['usuario_id'], dados['prestador_id'], dados['descricao_servico'], dados['valor'], dados['data_agendamento'], dados['status'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO pedidos (usuario_id, prestador_id, descricao_servico, valor, data_agendamento, status, data_pedido) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (pedido.usuario_id, pedido.prestador_id, pedido.descricao_servico, pedido.valor, pedido.data_agendamento, pedido.status, pedido.data_pedido))
        conn.commit()
        return jsonify({"message": "Pedido cadastrado!"}), 201
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/pedidos/<int:id>', methods=['GET'])
def buscar_pedido(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM pedidos WHERE id = %s", (id,))
        pedido = cursor.fetchone()
        if not pedido: return jsonify({"mensagem": "Pedido não encontrado."}), 404
        return jsonify(pedido), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/pedidos/<int:id>', methods=['DELETE'])
def excluir_pedido(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM pedidos WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Pedido não encontrado."}), 404
        return jsonify({"message": "Pedido excluído!"}), 200
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/avaliacoes', methods=['POST'])
def cadastrar_avaliacao():
    conn = None
    try:
        dados = request.get_json()
        avaliacao = Avaliacoes(dados['pedido_id'], dados['usuario_id'], dados['prestador_id'], dados['nota'], dados['comentario'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """INSERT INTO avaliacoes (pedido_id, usuario_id, prestador_id, nota, comentario, data_avaliacao) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (avaliacao.pedido_id, avaliacao.usuario_id, avaliacao.prestador_id, avaliacao.nota, avaliacao.comentario, avaliacao.data_avaliacao))
        conn.commit()
        return jsonify({"message": "Avaliação cadastrada!"}), 201
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/api/avaliacoes/<int:id>', methods=['PUT'])
def atualizar_avaliacao(id):
    conn = None
    try:
        dados = request.get_json()
        avaliacao = Avaliacoes(dados['pedido_id'], dados['usuario_id'], dados['prestador_id'], dados['nota'], dados['comentario'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE avaliacoes SET pedido_id=%s, usuario_id=%s, prestador_id=%s, nota=%s, comentario=%s, data_avaliacao=%s WHERE id=%s"""
        cursor.execute(sql, (avaliacao.pedido_id, avaliacao.usuario_id, avaliacao.prestador_id, avaliacao.nota, avaliacao.comentario, avaliacao.data_avaliacao, id))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Avaliação não encontrada."}), 404
        return jsonify({"message": "Avaliação atualizada!"}), 200
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
@app.route('/api/avaliacoes/<int:id>', methods=['DELETE'])
def excluir_avaliacao(id):
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM avaliacoes WHERE id = %s", (id,))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Avaliação não encontrada."}), 404
        return jsonify({"message": "Avaliação excluída!"}), 200
    except Exception as e:
        if conn: conn.rollback()
        return jsonify({"erro": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
            
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5500)