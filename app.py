import os
from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

CORS(app, resources={r"/api/*": {"origins":  "*", "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"]}})

db_config = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASS')
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

class Usuarios:
    def __init__(self, nome, email, cpf, telefone, endereco_usuario, aceitou_lgpd, data_consentimento, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone
        self.endereco_usuario = endereco_usuario
        self.aceitou_lgpd = aceitou_lgpd
        self.data_consentimento = data_consentimento
        
class Prestadores:
    def __init__(self, nome, email, cpf, telefone, endereco_prestador, categoria_servico, descricao, aceitou_lgpd, data_consentimento, id=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.cpf = cpf
        self.telefone = telefone
        self.endereco_prestador = endereco_prestador
        self.categoria_servico = categoria_servico
        self.descricao = descricao
        self.aceitou_lgpd = aceitou_lgpd
        self.data_consentimento = data_consentimento
        
class Pedidos:
    def __init__(self, usuario_id, prestador_id, descricao_servico, valor, data_agendamento, status, data_pedido, id=None):
        self.id = id
        self.usuario_id = usuario_id
        self.prestador_id = prestador_id
        self.descricao_servico = descricao_servico
        self.valor = valor
        self.data_agendamento = data_agendamento
        self.status = status
        self.data_pedido = data_pedido
        
class Avaliacoes:
    def __init__(self, pedido_id, usuario_id, prestador_id, nota, comentario, data_avaliacao, id=None):
        self.id = id
        self.pedido_id = pedido_id
        self.usuario_id = usuario_id
        self.prestador_id = prestador_id
        self.nota = nota
        self.comentario = comentario
        self.data_avaliacao = data_avaliacao
        
@app.route('/api/usuario', methods=['POST']) #serve 
def cadastrar_usuario():
    conn = None
    try:
        dados = request.get_json()
        usuario = Usuarios(dados['nome'], dados['email'], dados['cpf'], dados['telefone'], dados['endereco_usuario'], dados['aceitou_lgpd'], dados['data_consentimento'])
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO DimUsuarios (nome, email, cpf, telefone, endereco_usuario, aceitou_lgpd, data_consentimento) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (usuario.nome, usuario.email, usuario.cpf, usuario.telefone, usuario.endereco_usuario, usuario.aceitou_lgpd, usuario.data_consentimento))
        conn.commit()
        return jsonify({"message": "Usuário cadastrado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()