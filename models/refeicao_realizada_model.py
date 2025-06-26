from database.connection import get_connection

class RefeicaoRealizadaModel:
    @staticmethod
    def adicionar(id_refeicao, id_plano, id_prato):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO refeicoes_realizadas (id_refeicao, id_plano, id_prato, realizada)
            VALUES (?, ?, ?, 0)
        ''', (id_refeicao, id_plano, id_prato))
        conn.commit()
        conn.close()

    @staticmethod
    def marcar_como_realizada(id_refeicao, realizada):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE refeicoes_realizadas SET realizada = ? WHERE id_refeicao = ?
        ''', (realizada, id_refeicao))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_por_plano(id_plano):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT rr.id_refeicao, r.nome_refeicao, p.nome AS prato_nome, rr.realizada
            FROM refeicoes_realizadas rr
            JOIN refeicoes r ON r.id_refeicao = rr.id_refeicao
            JOIN pratos p ON p.id_prato = rr.id_prato
            WHERE rr.id_plano = ?
        ''', (id_plano,))
        return cursor.fetchall()

    @staticmethod
    def excluir(id_refeicao):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM refeicoes_realizadas WHERE id_refeicao = ?', (id_refeicao,))
        conn.commit()
        conn.close()

    @staticmethod
    def listar_historico_por_usuario(id_usuario):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.nome_refeicao, r.tipo, r.data, p.nome AS prato_nome, rr.realizada,
                   COALESCE(SUM(i.calorias_100g * pi.quantidade_gramas / 100), 0) AS calorias_totais
            FROM refeicoes_realizadas rr
            JOIN refeicoes r ON r.id_refeicao = rr.id_refeicao
            JOIN pratos p ON p.id_prato = rr.id_prato
            JOIN planos_diarios pd ON pd.id_plano = rr.id_plano
            LEFT JOIN prato_ingredientes pi ON pi.id_prato = p.id_prato
            LEFT JOIN ingredientes i ON i.id_ingrediente = pi.id_ingrediente
            WHERE pd.id_usuario = ?
            GROUP BY rr.id_refeicao, r.nome_refeicao, r.tipo, r.data, p.nome, rr.realizada
            ORDER BY r.data DESC, r.tipo
        ''', (id_usuario,))
        return cursor.fetchall()
