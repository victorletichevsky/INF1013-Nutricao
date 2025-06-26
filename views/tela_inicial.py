import tkinter as tk
from tkinter import messagebox, ttk
from controllers.usuario_controller import UsuarioController
from utils.session import set_usuario

class TelaInicial(tk.Frame):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent, bg="white")
        self.on_success_callback = on_success_callback

        tk.Label(self, text="Tela Inicial", font=("Arial", 20), bg="white").pack(pady=20)

        tk.Label(self, text="Nome do usuário:", bg="white").pack(pady=5)
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack(pady=5)

        tk.Label(self, text="Refeições por dia:", bg="white").pack(pady=5)
        self.entry_refeicoes = tk.Entry(self)
        self.entry_refeicoes.pack(pady=5)

        ttk.Button(self, text="Continuar", command=self.cadastrar_usuario).pack(pady=10)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get()
        refeicoes = self.entry_refeicoes.get()
        if not nome or not refeicoes:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        UsuarioController.registrar_usuario(nome, f"{nome}@example.com", "senha", int(refeicoes))
    
        usuario = UsuarioController.buscar_usuario_por_email(f"{nome}@example.com")
        set_usuario(usuario)

        messagebox.showinfo("Sucesso", "Usuário cadastrado!")
        self.on_success_callback()

