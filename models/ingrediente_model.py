import uuid
from database.connection import get_connection

class IngredienteModel:
    @staticmethod
    def create(nome, calorias_100g):
        conn = get_connection()
        cursor = conn.cursor()
        id_ingrediente = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO ingredientes (id_ingrediente, nome, calorias_100g)
            VALUES (?, ?, ?)
        ''', (id_ingrediente, nome, calorias_100g))
        conn.commit()
        conn.close()
        return id_ingrediente

    @staticmethod
    def get_all():
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ingredientes')
        ingredientes = cursor.fetchall()
        conn.close()
        return ingredientes
    
    @staticmethod
    def update(id_ingrediente, nome, calorias_100g):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE ingredientes
            SET nome = ?, calorias_100g = ?
            WHERE id_ingrediente = ?
        ''', (nome, calorias_100g, id_ingrediente))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_nome(nome):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM ingredientes WHERE nome = ?', (nome,))
        return cursor.fetchone()

