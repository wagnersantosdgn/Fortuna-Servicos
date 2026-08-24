-- Active: 1786965765172@@127.0.0.1@3306@sistema_servicos
DROP DATABASE IF EXISTS sistema_servicos;
CREATE DATABASE IF NOT EXISTS sistema_servicos;
USE sistema_servicos;

-- 1. Tabela de Usuários (Clientes)
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    cpf VARCHAR(255) NOT NULL UNIQUE, -- Armazenar criptografado (AES-256 / Hash)
    senha VARCHAR(255) NOT NULL,       -- Guardar sempre com hash (ex: bcrypt / argon2)
    telefone VARCHAR(20) NOT NULL,
    endereco_usuario VARCHAR(255) NOT NULL,
    -- CAMPOS OBRIGATÓRIOS PARA COMPLIANCE COM A LGPD:
    aceitou_lgpd BOOLEAN NOT NULL DEFAULT TRUE,    -- Prova que o cliente marcou a checkbox
    data_consentimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Registro exato de DATA e HORA do aceite
);

-- 2. Tabela de Prestadores de Serviço
CREATE TABLE prestadores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    cpf VARCHAR(255) NOT NULL UNIQUE, -- Armazenar criptografado (AES-256 / Hash)
    senha VARCHAR(255) NOT NULL,       -- Guardar sempre com hash (ex: bcrypt / argon2)
    telefone VARCHAR(20) NOT NULL,
    endereco_prestador VARCHAR(255) NOT NULL,
    categoria_servico VARCHAR(100) NOT NULL,
    descricao TEXT,
	-- CAMPOS OBRIGATÓRIOS PARA COMPLIANCE COM A LGPD:
    aceitou_lgpd BOOLEAN NOT NULL DEFAULT TRUE,    -- Prova que o cliente marcou a checkbox
    data_consentimento TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Registro exato de DATA e HORA do aceite
);

-- 3. Tabela de Pedidos
CREATE TABLE pedidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    prestador_id INT NOT NULL,
    descricao_servico TEXT (255) NOT NULL,
    valor DECIMAL(10, 2),
    data_agendamento DATETIME NOT NULL,
    status ENUM('Pendente', 'Em Andamento', 'Concluído', 'Cancelado') DEFAULT 'Pendente',
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Chaves Estrangeiras (Relacionamentos)
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (prestador_id) REFERENCES prestadores(id) ON DELETE CASCADE
);

-- 4. Tabela de Avaliações
CREATE TABLE avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pedido_id INT NOT NULL,
    usuario_id INT NOT NULL,
    prestador_id INT NOT NULL,
    nota INT CHECK (nota BETWEEN 1 AND 5),
    comentario TEXT (255),
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Chaves Estrangeiras (Relacionamentos)
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (prestador_id) REFERENCES prestadores(id) ON DELETE CASCADE
);

INSERT INTO usuarios (nome, email, cpf, senha, telefone, endereco_usuario, aceitou_lgpd, data_consentimento) VALUES ('Ana Souza', 'anasouza@email.com', '244.512.321-23', "0001", "+5531988432004", "Grau Técnico", TRUE, NOW());
INSERT INTO prestadores (nome, email, cpf, senha, telefone, endereco_prestador, categoria_servico, descricao, aceitou_lgpd, data_consentimento) VALUES ('anderson freire', 'andersonfreire@gmail.com', '000.054.000-00', "0002", "+5531988423005", "senac", "limpeza", "serviço de limpeza residencial e comercial", TRUE, NOW());
-- Consulta com JOIN para testar
SELECT
    pedidos.id,
    usuarios.nome AS Usuario,
    prestadores.nome AS prestador,
    pedidos.status
FROM pedidos
INNER JOIN usuarios ON pedidos.usuario_id = usuarios.id
INNER JOIN prestadores ON pedidos.prestador_id = prestadores.id;