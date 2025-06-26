from models.progresso_semanal_model import ProgressoSemanalModel
from datetime import datetime, date, timedelta

class ProgressoSemanalController:
    def __init__(self):
        self.model = ProgressoSemanalModel()
    
    def obter_progresso_semana_atual(self, id_usuario):
        return self.model.calcular_progresso_semana(id_usuario)
    
    def obter_progresso_semana_especifica(self, id_usuario, data_inicio):
        if isinstance(data_inicio, str):
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        return self.model.calcular_progresso_semana(id_usuario, data_inicio)
    
    def formatar_dados_para_exibicao(self, progresso):
        dados_formatados = []
        dias_semana = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for i, dia_data in enumerate(self._gerar_datas_semana(progresso['data_inicio'])):
            dia_dados = next((d for d in progresso['dados_diarios'] if str(d['data']) == str(dia_data)), None)
            
            dados_formatados.append({
                'dia_semana': dias_semana[i],
                'data': dia_data,
                'calorias': dia_dados['calorias_consumidas'] if dia_dados else 0,
                'refeicoes_realizadas': dia_dados['refeicoes_realizadas'] if dia_dados else 0,
                'refeicoes_planejadas': dia_dados['refeicoes_planejadas'] if dia_dados else 0
            })
        
        return dados_formatados
    
    def _gerar_datas_semana(self, data_inicio):
        return [data_inicio + timedelta(days=i) for i in range(7)]