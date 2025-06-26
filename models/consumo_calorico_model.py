from database.connection import get_connection
from datetime import datetime, date

class ConsumoCaloricoModel:
    @staticmethod
    def calcular_consumo_diario(id_usuario, data=None):
        if data is None:
            data = date.today()
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT SUM((i.calorias_100g * pi.quantidade_gramas) / 100.0) as total_calorias
            FROM refeicoes_realizadas rr
            JOIN planos_diarios pd ON pd.id_plano = rr.id_plano
            JOIN prato_ingredientes pi ON pi.id_prato = rr.id_prato
            JOIN ingredientes i ON i.id_ingrediente = pi.id_ingrediente
            WHERE pd.id_usuario = ? AND pd.data = ? AND rr.realizada = 1
        ''', (id_usuario, data))
        
        resultado = cursor.fetchone()
        conn.close()
        return resultado[0] if resultado[0] else 0

    @staticmethod
    def obter_historico_semanal(id_usuario, data_inicio, data_fim):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT pd.data, SUM((i.calorias_100g * pi.quantidade_gramas) / 100.0) as total_calorias
            FROM refeicoes_realizadas rr
            JOIN planos_diarios pd ON pd.id_plano = rr.id_plano
            JOIN prato_ingredientes pi ON pi.id_prato = rr.id_prato
            JOIN ingredientes i ON i.id_ingrediente = pi.id_ingrediente
            WHERE pd.id_usuario = ? AND pd.data BETWEEN ? AND ? AND rr.realizada = 1
            GROUP BY pd.data
            ORDER BY pd.data
        ''', (id_usuario, data_inicio, data_fim))
        
        resultados = cursor.fetchall()
        conn.close()
        return resultados