import uuid
from database.connection import get_connection

class PlanoDiarioModel:
    @staticmethod
    def get_by_data(id_usuario, data):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM planos_diarios WHERE id_usuario = ? AND data = ?',
            (id_usuario, data)
        )
        return cursor.fetchone()

    @staticmethod
    def create(id_usuario, data):
        conn = get_connection()
        cursor = conn.cursor()
        id_plano = str(uuid.uuid4())
        cursor.execute(
            'INSERT INTO planos_diarios (id_plano, id_usuario, data) VALUES (?, ?, ?)',
            (id_plano, id_usuario, data)
        )
        conn.commit()
        conn.close()
        return id_plano
