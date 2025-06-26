from database.connection import get_connection

class PratoIngredienteModel:
    @staticmethod
    def adicionar_ingrediente(id_prato, id_ingrediente, quantidade):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO prato_ingredientes (id_prato, id_ingrediente, quantidade_gramas)
            VALUES (?, ?, ?)
        ''', (id_prato, id_ingrediente, quantidade))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_ingredientes_do_prato(id_prato):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT i.nome, pi.quantidade_gramas, i.calorias_100g
            FROM prato_ingredientes pi
            JOIN ingredientes i ON i.id_ingrediente = pi.id_ingrediente
            WHERE pi.id_prato = ?
        ''', (id_prato,))
        return cursor.fetchall()

    @staticmethod
    def remover_ingrediente(id_prato, nome_ingrediente):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            DELETE FROM prato_ingredientes
            WHERE id_prato = ? AND id_ingrediente = (
                SELECT id_ingrediente FROM ingredientes WHERE nome = ?
            )
        ''', (id_prato, nome_ingrediente))
        conn.commit()
        conn.close()
