import uuid
from database.connection import get_connection

class UsuarioModel:
    @staticmethod
    def create(nome, email, senha, refeicoes_por_dia):
        conn = get_connection()
        cursor = conn.cursor()
        id_usuario = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO usuario (id_usuario, nome, email, senha, refeicoes_por_dia)
            VALUES (?, ?, ?, ?, ?)
        ''', (id_usuario, nome, email, senha, refeicoes_por_dia))
        conn.commit()
        conn.close()
        return id_usuario

    @staticmethod
    def get_by_email(email):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario WHERE email = ?', (email,))
        usuario = cursor.fetchone()
        conn.close()
        return usuario
    
    @staticmethod
    def get_primeiro_usuario():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuario LIMIT 1')
        usuario = cursor.fetchone()
        conn.close()
        return usuario

