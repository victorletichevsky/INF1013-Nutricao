from models.plano_diario_model import PlanoDiarioModel
from models.refeicao_model import RefeicaoModel
from models.refeicao_realizada_model import RefeicaoRealizadaModel

class PlanoDiarioController:
    @staticmethod
    def obter_ou_criar_plano(id_usuario, data):
        plano = PlanoDiarioModel.get_by_data(id_usuario, data)
        if plano:
            return plano["id_plano"]
        return PlanoDiarioModel.create(id_usuario, data)

    @staticmethod
    def adicionar_refeicao(id_plano, nome_refeicao, tipo, data, id_prato):
        id_refeicao = RefeicaoModel.create(nome_refeicao, tipo, data)
        RefeicaoRealizadaModel.adicionar(id_refeicao, id_plano, id_prato)

    @staticmethod
    def listar_refeicoes(id_plano):
        return RefeicaoRealizadaModel.listar_por_plano(id_plano)

    @staticmethod
    def marcar_realizada(id_refeicao, realizada):
        RefeicaoRealizadaModel.marcar_como_realizada(id_refeicao, realizada)

    @staticmethod
    def excluir_refeicao(id_refeicao):
        RefeicaoRealizadaModel.excluir(id_refeicao)
        RefeicaoModel.delete(id_refeicao)
