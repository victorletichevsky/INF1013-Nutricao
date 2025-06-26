import tkinter as tk
from tkinter import ttk
from .tela_ingredientes import TelaIngredientes
from .tela_pratos import TelaPratos
from .tela_plano_diario import TelaPlanoDiario
from .tela_historico import TelaHistorico

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.sidebar_frame = tk.Frame(self, width=200, bg="#f0f0f0")
        self.sidebar_frame.pack(side="left", fill="y")

        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="right", expand=True, fill="both")

        self.create_sidebar_buttons()

    def create_sidebar_buttons(self):
        buttons = [
            ("Plano Diário", self.open_plano_diario),
            ("Progresso Semanal", self.open_progresso_semanal),
            ("Lista de Pratos", self.open_lista_pratos),
            ("Ingredientes", self.open_ingredientes),
            ("Consumo Calórico", self.open_consumo_calorico),
            ("Histórico de Refeições", self.open_historico_refeicoes),
        ]

        for (text, command) in buttons:
            btn = ttk.Button(self.sidebar_frame, text=text, command=command)
            btn.pack(pady=10, padx=10, fill='x')

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def open_plano_diario(self):
        self.clear_content()
        TelaPlanoDiario(self.content_frame).pack(expand=True, fill="both")

    def open_progresso_semanal(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Progresso Semanal", font=("Arial", 18), bg="white").pack(pady=20)

    def open_lista_pratos(self):
        self.clear_content()
        TelaPratos(self.content_frame).pack(expand=True, fill="both")

    def open_ingredientes(self):
        self.clear_content()
        TelaIngredientes(self.content_frame).pack(expand=True, fill="both")

    def open_consumo_calorico(self):
        self.clear_content()
        tk.Label(self.content_frame, text="Consumo Calórico", font=("Arial", 18), bg="white").pack(pady=20)

    def open_historico_refeicoes(self):
        self.clear_content()
        TelaHistorico(self.content_frame).pack(expand=True, fill="both")
