from models.prato_model import PratoModel
from models.prato_ingrediente_model import PratoIngredienteModel

class PratoController:
    @staticmethod
    def criar_prato(nome, id_usuario):
        return PratoModel.create(nome, id_usuario)

    @staticmethod
    def atualizar_prato(id_prato, novo_nome):
        PratoModel.update(id_prato, novo_nome)

    @staticmethod
    def listar_pratos(id_usuario):
        return PratoModel.get_all_by_usuario(id_usuario)

    @staticmethod
    def adicionar_ingrediente(id_prato, id_ingrediente, quantidade):
        PratoIngredienteModel.adicionar_ingrediente(id_prato, id_ingrediente, quantidade)

    @staticmethod
    def listar_ingredientes_do_prato(id_prato):
        return PratoIngredienteModel.listar_ingredientes_do_prato(id_prato)

    @staticmethod
    def remover_ingrediente(id_prato, nome_ingrediente):
        PratoIngredienteModel.remover_ingrediente(id_prato, nome_ingrediente)

    @staticmethod
    def excluir_prato(id_prato):
        PratoModel.delete(id_prato)
