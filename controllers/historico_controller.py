from models.refeicao_realizada_model import RefeicaoRealizadaModel

class HistoricoController:
    @staticmethod
    def listar_historico_usuario(id_usuario):
        return RefeicaoRealizadaModel.listar_historico_por_usuario(id_usuario)