from database.connection import get_connection
from datetime import datetime, date, timedelta

class ProgressoSemanalModel:
    @staticmethod
    def calcular_progresso_semana(id_usuario, data_inicio=None):
        if data_inicio is None:
            hoje = date.today()
            data_inicio = hoje - timedelta(days=hoje.weekday())
        
        data_fim = data_inicio + timedelta(days=6)
        
        conn = get_connection()
        cursor = conn.cursor()
        
        # Consumo calórico por dia da semana
        cursor.execute('''
            SELECT pd.data, 
                   COALESCE(SUM((i.calorias_100g * pi.quantidade_gramas) / 100.0), 0) as calorias_consumidas,
                   COUNT(DISTINCT CASE WHEN rr.realizada = 1 THEN rr.id_refeicao END) as refeicoes_realizadas,
                   COUNT(DISTINCT rr.id_refeicao) as refeicoes_planejadas
            FROM planos_diarios pd
            LEFT JOIN refeicoes_realizadas rr ON pd.id_plano = rr.id_plano
            LEFT JOIN prato_ingredientes pi ON pi.id_prato = rr.id_prato
            LEFT JOIN ingredientes i ON i.id_ingrediente = pi.id_ingrediente
            WHERE pd.id_usuario = ? AND pd.data BETWEEN ? AND ?
            GROUP BY pd.data
            ORDER BY pd.data
        ''', (id_usuario, data_inicio, data_fim))
        
        dados_diarios = cursor.fetchall()
        conn.close()
        
        return {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'dados_diarios': dados_diarios,
            'resumo': ProgressoSemanalModel._calcular_resumo(dados_diarios)
        }
    
    @staticmethod
    def _calcular_resumo(dados_diarios):
        if not dados_diarios:
            return {
                'total_calorias': 0,
                'media_calorias': 0,
                'total_refeicoes_realizadas': 0,
                'total_refeicoes_planejadas': 0,
                'taxa_cumprimento': 0
            }
        
        total_calorias = sum(dia['calorias_consumidas'] for dia in dados_diarios)
        total_refeicoes_realizadas = sum(dia['refeicoes_realizadas'] for dia in dados_diarios)
        total_refeicoes_planejadas = sum(dia['refeicoes_planejadas'] for dia in dados_diarios)
        
        return {
            'total_calorias': total_calorias,
            'media_calorias': total_calorias / len(dados_diarios),
            'total_refeicoes_realizadas': total_refeicoes_realizadas,
            'total_refeicoes_planejadas': total_refeicoes_planejadas,
            'taxa_cumprimento': (total_refeicoes_realizadas / total_refeicoes_planejadas * 100) if total_refeicoes_planejadas > 0 else 0
        }