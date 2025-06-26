import tkinter as tk
from tkinter import ttk, messagebox
from controllers.historico_controller import HistoricoController
from utils.session import get_usuario
from utils.tipos_refeicao import obter_nome_tipo

class TelaHistorico(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        tk.Label(self, text="Histórico de Refeições", font=("Arial", 18), bg="white").pack(pady=10)

        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 12))
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        
        self.tree = ttk.Treeview(self, columns=("Nome", "Tipo", "Data", "Prato", "Calorias", "Status"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Tipo", text="Tipo")
        self.tree.heading("Data", text="Data")
        self.tree.heading("Prato", text="Prato")
        self.tree.heading("Calorias", text="Calorias")
        self.tree.heading("Status", text="Status")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.carregar_historico()

    def carregar_historico(self):
        usuario = get_usuario()
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        historico = HistoricoController.listar_historico_usuario(usuario["id_usuario"])
        
        for refeicao in historico:
            status = "✅" if refeicao["realizada"] else "❌"
            calorias = f"{refeicao['calorias_totais']:.1f} kcal"
            tipo_nome = obter_nome_tipo(refeicao["tipo"])
            self.tree.insert("", "end", values=(
                refeicao["nome_refeicao"],
                tipo_nome,
                refeicao["data"],
                refeicao["prato_nome"],
                calorias,
                status
            ))