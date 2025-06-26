import tkinter as tk
from views.main_window import MainWindow
from views.tela_inicial import TelaInicial
from controllers.usuario_controller import UsuarioController
from utils.session import set_usuario

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicativo Nutrição")
        self.geometry("900x600")
        self.configure(bg="white")

        self.check_usuario()

    def check_usuario(self):
        usuario = UsuarioController.buscar_primeiro_usuario()
        if usuario:
            set_usuario(usuario)
            self.exibir_main_window()
        else:
            self.exibir_tela_inicial()

    def exibir_main_window(self):
        self.clear_tela_atual()
        main_window = MainWindow(self)
        main_window.pack(expand=True, fill="both")

    def exibir_tela_inicial(self):
        self.clear_tela_atual()
        tela_inicial = TelaInicial(self, self.exibir_main_window)
        tela_inicial.pack(expand=True, fill="both")

    def clear_tela_atual(self):
        for widget in self.winfo_children():
            widget.destroy()
            
if __name__ == "__main__":
    app = App()
    app.mainloop()
