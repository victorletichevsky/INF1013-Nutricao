import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from utils.session import get_usuario
from controllers.plano_diario_controller import PlanoDiarioController
from controllers.prato_controller import PratoController

class TelaPlanoDiario(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.id_plano = None

        tk.Label(self, text="Plano Diário", font=("Arial", 18), bg="white").pack(pady=10)

        self.data_var = tk.StringVar(value=str(date.today()))
        tk.Label(self, text="Data (YYYY-MM-DD):", bg="white").pack()
        tk.Entry(self, textvariable=self.data_var).pack()

        ttk.Button(self, text="Carregar plano", command=self.carregar_plano).pack(pady=10)

        self.frame_adicionar = tk.Frame(self, bg="white")
        self.frame_adicionar.pack(pady=10)

        tk.Label(self.frame_adicionar, text="Nome da refeição:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome_refeicao = tk.Entry(self.frame_adicionar)
        self.entry_nome_refeicao.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_adicionar, text="Tipo (0=Café, 1=Almoço...):", bg="white").grid(row=1, column=0)
        self.entry_tipo = tk.Entry(self.frame_adicionar)
        self.entry_tipo.grid(row=1, column=1)

        tk.Label(self.frame_adicionar, text="Prato:", bg="white").grid(row=2, column=0)
        self.combo_pratos = ttk.Combobox(self.frame_adicionar, state="readonly")
        self.combo_pratos.grid(row=2, column=1)

        ttk.Button(self.frame_adicionar, text="Adicionar refeição", command=self.adicionar_refeicao).grid(row=3, columnspan=2, pady=10)

        self.lista = tk.Listbox(self)
        self.lista.pack(fill="x", padx=20, pady=10)

        ttk.Button(self, text="Marcar como realizada", command=self.marcar_realizada).pack(pady=5)

    def carregar_plano(self):
        usuario = get_usuario()
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        data_selecionada = self.data_var.get()
        self.id_plano = PlanoDiarioController.obter_ou_criar_plano(usuario["id_usuario"], data_selecionada)
        self.carregar_pratos()
        self.carregar_refeicoes()

    def carregar_pratos(self):
        usuario = get_usuario()
        pratos = PratoController.listar_pratos(usuario["id_usuario"])
        self.dict_pratos = {p["nome"]: p["id_prato"] for p in pratos}
        self.combo_pratos["values"] = list(self.dict_pratos.keys())

    def adicionar_refeicao(self):
        if not self.id_plano:
            messagebox.showwarning("Aviso", "Carregue um plano antes.")
            return

        nome = self.entry_nome_refeicao.get()
        tipo = self.entry_tipo.get()
        prato_nome = self.combo_pratos.get()

        if not nome or not tipo or not prato_nome:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            tipo = int(tipo)
        except ValueError:
            messagebox.showerror("Erro", "Tipo deve ser um número.")
            return

        id_prato = self.dict_pratos[prato_nome]
        PlanoDiarioController.adicionar_refeicao(self.id_plano, nome, tipo, self.data_var.get(), id_prato)
        self.carregar_refeicoes()

    def carregar_refeicoes(self):
        self.lista.delete(0, tk.END)
        refeicoes = PlanoDiarioController.listar_refeicoes(self.id_plano)
        self.dict_refeicoes = {}

        for r in refeicoes:
            desc = f"{r['nome_refeicao']} - {r['prato_nome']} - {'OK' if r['realizada'] else 'PENDENTE'}"
            self.lista.insert(tk.END, desc)
            self.dict_refeicoes[desc] = r["id_refeicao"]

    def marcar_realizada(self):
        sel = self.lista.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma refeição.")
            return
        texto = self.lista.get(sel[0])
        id_refeicao = self.dict_refeicoes[texto]
        PlanoDiarioController.marcar_realizada(id_refeicao, 1)
        self.carregar_refeicoes()
