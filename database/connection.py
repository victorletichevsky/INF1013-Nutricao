import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'app.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS usuario (
        id_usuario TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL,
        refeicoes_por_dia INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS ingredientes (
        id_ingrediente TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        calorias_100g REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS pratos (
        id_prato TEXT PRIMARY KEY,
        nome TEXT NOT NULL,
        id_usuario TEXT NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    );

    CREATE TABLE IF NOT EXISTS prato_ingredientes (
        id_prato TEXT NOT NULL,
        id_ingrediente TEXT NOT NULL,
        quantidade_gramas REAL,
        PRIMARY KEY (id_prato, id_ingrediente),
        FOREIGN KEY (id_prato) REFERENCES pratos(id_prato),
        FOREIGN KEY (id_ingrediente) REFERENCES ingredientes(id_ingrediente)
    );

    CREATE TABLE IF NOT EXISTS planos_diarios (
        id_plano TEXT PRIMARY KEY,
        id_usuario TEXT NOT NULL,
        data DATE NOT NULL,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    );

    CREATE TABLE IF NOT EXISTS refeicoes (
        id_refeicao TEXT PRIMARY KEY,
        nome_refeicao TEXT NOT NULL,
        data DATE NOT NULL,
        tipo INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS refeicoes_realizadas (
        id_refeicao TEXT PRIMARY KEY,
        id_plano TEXT,
        id_prato TEXT,
        realizada BOOLEAN NOT NULL DEFAULT 0,
        FOREIGN KEY (id_plano) REFERENCES planos_diarios(id_plano),
        FOREIGN KEY (id_prato) REFERENCES pratos(id_prato)
    );

    CREATE TABLE IF NOT EXISTS meta (
        id TEXT PRIMARY KEY,
        id_usuario TEXT NOT NULL,
        dataCriacao DATE NOT NULL,
        caloriasTotais INTEGER,
        numRefeicoesRealizadas INTEGER,
        numRefeicoesPlanejadas INTEGER,
        FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
    );
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Banco de dados inicializado!")
