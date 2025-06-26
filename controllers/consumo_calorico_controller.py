from models.consumo_calorico_model import ConsumoCaloricoModel
from datetime import date, timedelta

from models.consumo_calorico_model import ConsumoCaloricoModel
from datetime import date, timedelta

class ConsumoCaloricoController:
    @staticmethod
    def obter_consumo_hoje(id_usuario):
        return ConsumoCaloricoModel.calcular_consumo_diario(id_usuario)
    
    @staticmethod
    def obter_consumo_data(id_usuario, data):
        return ConsumoCaloricoModel.calcular_consumo_diario(id_usuario, data)
    
    @staticmethod
    def obter_historico_semana(id_usuario):
        hoje = date.today()
        inicio_semana = hoje - timedelta(days=6)
        return ConsumoCaloricoModel.obter_historico_semanal(id_usuario, inicio_semana, hoje)