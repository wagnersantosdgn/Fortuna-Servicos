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

def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))
    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False
    soma_1 = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto_1 = (soma_1 * 10) % 11
    digito_1 = 0 if resto_1 in (10, 11) else resto_1
    soma_2 = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto_2 = (soma_2 * 10) % 11
    digito_2 = 0 if resto_2 in (10, 11) else resto_2
    return cpf[-2:] == f"{digito_1}{digito_2}"
def validar_telefone(telefone):
    telefone_numeros = re.sub(r'\D', '', str(telefone))
    return len(telefone_numeros) in (10, 11) and telefone_numeros[0] != '0'
class Usuarios:
    def __init__(self, nome, email, cpf, senha, telefone, endereco_usuario, aceitou_lgpd, id=None):
        if not validar_cpf(cpf):
            return jsonify({"erro": "CPF inválido."}), 400
        if not validar_telefone(telefone):
            return jsonify({"erro": "Telefone inválido."}), 400
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
        if not validar_cpf(cpf):
            return jsonify({"erro": "CPF inválido."}), 400
        if not validar_telefone(telefone):
            return jsonify({"erro": "Telefone inválido."}), 400
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
        usuario = Usuarios(dados['nome'], dados['email'], dados['cpf'], dados['senha'], dados['telefone'], dados['endereco_usuario'], dados['aceitou_lgpd'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO usuarios (nome, email, cpf, senha, telefone, endereco_usuario, aceitou_lgpd, data_consentimento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.cpf, usuario.senha, usuario.telefone, usuario.endereco_usuario, usuario.aceitou_lgpd, usuario.data_consentimento))
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
        usuario = Usuarios(dados['nome'], dados['email'], dados['cpf'], dados['senha'], dados['telefone'], dados['endereco_usuario'], dados['aceitou_lgpd'], dados['data_consentimento'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE usuarios SET nome=%s, email=%s, cpf=%s, senha=%s, telefone=%s, endereco_usuario=%s, aceitou_lgpd=%s, data_consentimento=%s WHERE id=%s"""
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.cpf, usuario.senha, usuario.telefone, usuario.endereco_usuario, usuario.aceitou_lgpd, usuario.data_consentimento, id))
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
        prestador = Prestadores(dados['nome'], dados['email'], dados['cpf'], dados['senha'], dados['telefone'], dados['endereco_prestador'], dados['categoria_servico'], dados['descricao'], dados['aceitou_lgpd'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO prestadores (nome, email, cpf, senha, telefone, endereco_prestador, categoria_servico, descricao, aceitou_lgpd, data_consentimento) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (prestador.nome, prestador.email, prestador.cpf, prestador.senha, prestador.telefone, prestador.endereco_prestador, prestador.categoria_servico, prestador.descricao, prestador.aceitou_lgpd, prestador.data_consentimento))
        conn.commit()
        return jsonify({"message": "Prestador cadastrado com sucesso!"}), 201
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
        prestador = Prestadores(dados['nome'], dados['email'], dados['cpf'], dados['senha'], dados['telefone'], dados['endereco_prestador'], dados['categoria_servico'], dados['descricao'], dados['aceitou_lgpd'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """UPDATE prestadores SET nome=%s, email=%s, cpf=%s, senha=%s, telefone=%s, endereco_prestador=%s, categoria_servico=%s, descricao=%s, aceitou_lgpd=%s, data_consentimento=%s WHERE id=%s"""
        cursor.execute(sql, (prestador.nome, prestador.email, prestador.cpf, prestador.senha, prestador.telefone, prestador.endereco_prestador, prestador.categoria_servico, prestador.descricao, prestador.aceitou_lgpd, prestador.data_consentimento, id))
        conn.commit()
        if cursor.rowcount == 0: return jsonify({"mensagem": "Prestador não encontrado."}), 404
        return jsonify({"message": "Os dados foram atualizados!"}), 200
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