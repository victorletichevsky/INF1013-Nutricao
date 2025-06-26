import uuid
from database.connection import get_connection

class PratoModel:
    @staticmethod
    def create(nome, id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        id_prato = str(uuid.uuid4())
        cursor.execute('''
            INSERT INTO pratos (id_prato, nome, id_usuario)
            VALUES (?, ?, ?)
        ''', (id_prato, nome, id_usuario))
        conn.commit()
        conn.close()
        return id_prato

    @staticmethod
    def update(id_prato, novo_nome):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE pratos SET nome = ? WHERE id_prato = ?
        ''', (novo_nome, id_prato))
        conn.commit()
        conn.close()

    @staticmethod
    def get_all_by_usuario(id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM pratos WHERE id_usuario = ? ORDER BY nome
        ''', (id_usuario,))
        pratos = cursor.fetchall()
        conn.close()
        return pratos

    @staticmethod
    def delete(id_prato):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM prato_ingredientes WHERE id_prato = ?', (id_prato,))
        cursor.execute('DELETE FROM pratos WHERE id_prato = ?', (id_prato,))
        conn.commit()
        conn.close()
