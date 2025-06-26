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
        
        # Consumo calórico por dia da semana - filtrando datas válidas
        cursor.execute('''
            SELECT pd.data, 
                   COALESCE(SUM(CASE WHEN rr.realizada = 1 THEN (i.calorias_100g * pi.quantidade_gramas) / 100.0 ELSE 0 END), 0) as calorias_consumidas,
                   COUNT(DISTINCT CASE WHEN rr.realizada = 1 THEN rr.id_refeicao END) as refeicoes_realizadas,
                   COUNT(DISTINCT CASE WHEN rr.id_refeicao IS NOT NULL THEN rr.id_refeicao END) as refeicoes_planejadas
            FROM planos_diarios pd
            LEFT JOIN refeicoes_realizadas rr ON pd.id_plano = rr.id_plano
            LEFT JOIN prato_ingredientes pi ON pi.id_prato = rr.id_prato
            LEFT JOIN ingredientes i ON i.id_ingrediente = pi.id_ingrediente
            WHERE pd.id_usuario = ? AND pd.data BETWEEN ? AND ? AND LENGTH(pd.data) = 10
            GROUP BY pd.data
            ORDER BY pd.data
        ''', (id_usuario, data_inicio, data_fim))
        
        dados_diarios = cursor.fetchall()
        conn.close()
        
        # Garantir que todos os dias da semana estejam representados
        dados_completos = ProgressoSemanalModel._preencher_dias_faltantes(dados_diarios, data_inicio)
        
        return {
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'dados_diarios': dados_completos,
            'resumo': ProgressoSemanalModel._calcular_resumo(dados_completos)
        }
    
    @staticmethod
    def _preencher_dias_faltantes(dados_diarios, data_inicio):
        # Criar dicionário dos dados existentes
        dados_dict = {str(dia['data']): dia for dia in dados_diarios}
        
        # Preencher todos os 7 dias da semana
        dados_completos = []
        for i in range(7):
            data_dia = data_inicio + timedelta(days=i)
            data_str = str(data_dia)
            
            if data_str in dados_dict:
                dados_completos.append(dados_dict[data_str])
            else:
                # Criar entrada vazia para dias sem dados
                dados_completos.append({
                    'data': data_str,
                    'calorias_consumidas': 0,
                    'refeicoes_realizadas': 0,
                    'refeicoes_planejadas': 0
                })
        
        return dados_completos
    
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
            'media_calorias': total_calorias / 7,  # Sempre dividir por 7 dias
            'total_refeicoes_realizadas': total_refeicoes_realizadas,
            'total_refeicoes_planejadas': total_refeicoes_planejadas,
            'taxa_cumprimento': (total_refeicoes_realizadas / total_refeicoes_planejadas * 100) if total_refeicoes_planejadas > 0 else 0
        }