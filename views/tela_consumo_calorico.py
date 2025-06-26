import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
from controllers.consumo_calorico_controller import ConsumoCaloricoController
from models.usuario_model import UsuarioModel

class TelaConsumoCalórico(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        
        self.usuario = UsuarioModel.get_primeiro_usuario()
        if not self.usuario:
            tk.Label(self, text="Nenhum usuário encontrado", font=("Arial", 14), bg="white").pack(pady=20)
            return
            
        self.setup_ui()
        self.atualizar_dados()
    
    def setup_ui(self):
        # Título
        tk.Label(self, text="Consumo Calórico", font=("Arial", 18), bg="white").pack(pady=10)
        
        # Frame principal
        main_frame = tk.Frame(self, bg="white")
        main_frame.pack(fill="both", expand=True, padx=20)
        
        # Consumo de hoje
        hoje_frame = tk.LabelFrame(main_frame, text="Consumo de Hoje", font=("Arial", 12), bg="white")
        hoje_frame.pack(fill="x", pady=10)
        
        self.label_consumo_hoje = tk.Label(hoje_frame, text="0 kcal", font=("Arial", 16, "bold"), bg="white")
        self.label_consumo_hoje.pack(pady=10)
        
        # Histórico semanal
        historico_frame = tk.LabelFrame(main_frame, text="Histórico dos Últimos 7 Dias", font=("Arial", 12), bg="white")
        historico_frame.pack(fill="x", expand=True, pady=10)
        
        # Tabela do histórico
        self.tree_historico = ttk.Treeview(historico_frame, columns=("Data", "Calorias"), show="headings", height=7)
        self.tree_historico.heading("Data", text="Data")
        self.tree_historico.heading("Calorias", text="Calorias (kcal)")
        self.tree_historico.column("Data", width=150)
        self.tree_historico.column("Calorias", width=150)
        self.tree_historico.pack(pady=10, fill="x")
        
        
        # Botão atualizar
        ttk.Button(main_frame, text="Atualizar", command=self.atualizar_dados).pack(pady=10)
    
    def atualizar_dados(self):
        if not self.usuario:
            return
            
        id_usuario = self.usuario[0]  # Assumindo que o ID é o primeiro campo
        
        # Atualizar consumo de hoje
        consumo_hoje = ConsumoCaloricoController.obter_consumo_hoje(id_usuario)
        self.label_consumo_hoje.config(text=f"{consumo_hoje:.0f} kcal")
        
        # Atualizar histórico semanal
        self.atualizar_historico_semanal(id_usuario)
        
    
    def atualizar_historico_semanal(self, id_usuario):
        # Limpar tabela
        for item in self.tree_historico.get_children():
            self.tree_historico.delete(item)
        
        # Obter dados
        historico = ConsumoCaloricoController.obter_historico_semana(id_usuario)
        
        # Criar dicionário para facilitar busca
        dados_historico = {str(data): calorias for data, calorias in historico}
        
        # Preencher últimos 7 dias (incluindo dias sem dados)
        hoje = date.today()
        for i in range(6, -1, -1):
            data_dia = hoje - timedelta(days=i)
            data_str = str(data_dia)
            calorias = dados_historico.get(data_str, 0)
            
            self.tree_historico.insert("", "end", values=(
                data_dia.strftime("%d/%m/%Y"),
                f"{calorias:.0f}"
            ))