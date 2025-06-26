import uuid
from database.connection import get_connection

class RefeicaoModel:
    @staticmethod
    def create(nome_refeicao, tipo, data):
        conn = get_connection()
        cursor = conn.cursor()
        id_refeicao = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO refeicoes (id_refeicao, nome_refeicao, tipo, data)
            VALUES (?, ?, ?, ?)
        ''', (id_refeicao, nome_refeicao, tipo, data))
        conn.commit()
        conn.close()
        return id_refeicao

    @staticmethod
    def delete(id_refeicao):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM refeicoes WHERE id_refeicao = ?', (id_refeicao,))
        conn.commit()
        conn.close()
