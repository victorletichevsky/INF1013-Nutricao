from models.ingrediente_model import IngredienteModel
from models.usuario_model import UsuarioModel

class UsuarioController:
    @staticmethod
    def registrar_usuario(nome, email, senha, refeicoes_por_dia):
        return UsuarioModel.create(nome, email, senha, refeicoes_por_dia)

    @staticmethod
    def buscar_usuario_por_email(email):
        return UsuarioModel.get_by_email(email)
    
    @staticmethod
    def buscar_primeiro_usuario():
        return UsuarioModel.get_primeiro_usuario()
    
    @staticmethod
    def editar_ingrediente(id_ingrediente, nome, calorias):
        return IngredienteModel.update(id_ingrediente, nome, calorias)

