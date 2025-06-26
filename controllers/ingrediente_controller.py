from models.ingrediente_model import IngredienteModel

class IngredienteController:
    @staticmethod
    def adicionar_ingrediente(nome, calorias):
        return IngredienteModel.create(nome, calorias)

    @staticmethod
    def listar_ingredientes():
        return IngredienteModel.get_all()
    
    
