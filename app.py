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

class Usuarios:
    def __init__(self, nome, email, cpf, telefone, endereco_usuario, id=None):
        
class Prestadores:
    def __init__(self, nome, email, cpf, telefone, endereco_prestador, categoria_servico, descricao, id=None):
        
class Pedidos:
    def __init__(self, ):
        
class Avaliacoes:
    def __init__(self, ):