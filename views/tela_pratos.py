import tkinter as tk
from tkinter import ttk, messagebox
from controllers.prato_controller import PratoController
from controllers.ingrediente_controller import IngredienteController
from utils.session import get_usuario  

class TelaPratos(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        self.id_prato_em_edicao = None

        tk.Label(self, text="Pratos", font=("Arial", 18), bg="white").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.column("ID", width=0, stretch=False)
        self.tree.pack(padx=10, pady=10, fill="x")
        self.tree.bind("<Double-1>", self.selecionar_prato)

        self.form_frame = tk.Frame(self, bg="white")
        self.form_frame.pack(pady=10)

        tk.Label(self.form_frame, text="Nome do prato:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(self.form_frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        self.btn_salvar = ttk.Button(self.form_frame, text="Adicionar Prato", command=self.salvar_prato)
        self.btn_salvar.grid(row=1, column=0, pady=10, padx=5)
        
        self.btn_excluir_prato = ttk.Button(self.form_frame, text="Excluir Prato", command=self.excluir_prato)
        self.btn_excluir_prato.grid(row=1, column=1, pady=10, padx=5)

        self.ingrediente_frame = tk.Frame(self, bg="white")
        self.ingrediente_frame.pack(pady=10)

        tk.Label(self.ingrediente_frame, text="Ingrediente:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.combo_ingredientes = ttk.Combobox(self.ingrediente_frame, state="readonly")
        self.combo_ingredientes.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.ingrediente_frame, text="Quantidade (g):", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.entry_quantidade = tk.Entry(self.ingrediente_frame)
        self.entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

        self.btn_adicionar_ingrediente = ttk.Button(
            self.ingrediente_frame, text="Adicionar ao prato", command=self.adicionar_ingrediente_ao_prato)
        self.btn_adicionar_ingrediente.grid(row=2, columnspan=2, pady=10)

        self.label_calorias = tk.Label(self, text="", font=("Arial", 12), bg="white")
        self.label_calorias.pack(pady=5)

        self.lista_ingredientes = tk.Listbox(self)
        self.lista_ingredientes.pack(pady=10, fill="x", padx=10)

        # Frame para excluir ingrediente do prato
        self.excluir_frame = tk.Frame(self, bg="white")
        self.excluir_frame.pack(pady=10)

        tk.Label(self.excluir_frame, text="Excluir ingrediente:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.combo_ingredientes_prato = ttk.Combobox(self.excluir_frame, state="readonly")
        self.combo_ingredientes_prato.grid(row=0, column=1, padx=5, pady=5)

        self.btn_excluir_ingrediente = ttk.Button(
            self.excluir_frame, text="Excluir do prato", command=self.excluir_ingrediente_do_prato)
        self.btn_excluir_ingrediente.grid(row=0, column=2, padx=5, pady=5)

        self.atualizar_lista()
        self.carregar_ingredientes_combo()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        usuario = get_usuario()
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        pratos = PratoController.listar_pratos(usuario["id_usuario"])
        for prato in pratos:
            self.tree.insert("", "end", values=(prato["id_prato"], prato["nome"]))

    def carregar_ingredientes_combo(self):
        ingredientes = IngredienteController.listar_ingredientes()
        self.ingredientes_dict = {i["nome"]: i["id_ingrediente"] for i in ingredientes}
        self.combo_ingredientes["values"] = list(self.ingredientes_dict.keys())

    def salvar_prato(self):
        nome = self.entry_nome.get().strip()
        if not nome:
            messagebox.showwarning("Aviso", "Informe o nome do prato.")
            return

        usuario = get_usuario()
        if not usuario:
            messagebox.showerror("Erro", "Usuário não encontrado.")
            return

        if self.id_prato_em_edicao:
            PratoController.atualizar_prato(self.id_prato_em_edicao, nome)
            messagebox.showinfo("Atualizado", "Prato atualizado com sucesso.")
        else:
            self.id_prato_em_edicao = PratoController.criar_prato(nome, usuario["id_usuario"])
            messagebox.showinfo("Adicionado", "Prato criado com sucesso.")

        self.entry_nome.delete(0, tk.END)
        self.btn_salvar.config(text="Adicionar Prato")
        self.atualizar_lista()

    def selecionar_prato(self, event):
        item = self.tree.selection()
        if not item:
            return
        values = self.tree.item(item, "values")
        self.id_prato_em_edicao = values[0]
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, values[1])
        self.btn_salvar.config(text="Salvar Nome")
        self.atualizar_ingredientes_do_prato()

    def adicionar_ingrediente_ao_prato(self):
        if not self.id_prato_em_edicao:
            messagebox.showwarning("Aviso", "Crie ou selecione um prato primeiro.")
            return

        nome_ingrediente = self.combo_ingredientes.get()
        qtd_texto = self.entry_quantidade.get()

        if nome_ingrediente not in self.ingredientes_dict or not qtd_texto:
            messagebox.showwarning("Aviso", "Preencha corretamente os campos.")
            return

        try:
            qtd = float(qtd_texto)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade inválida.")
            return

        id_ing = self.ingredientes_dict[nome_ingrediente]
        PratoController.adicionar_ingrediente(self.id_prato_em_edicao, id_ing, qtd)
        self.entry_quantidade.delete(0, tk.END)
        self.atualizar_ingredientes_do_prato()

    def atualizar_ingredientes_do_prato(self):
        self.lista_ingredientes.delete(0, tk.END)
        ingredientes = PratoController.listar_ingredientes_do_prato(self.id_prato_em_edicao)
        total_calorias = 0
        nomes_ingredientes = []

        for ing in ingredientes:
            cal = ing["calorias_100g"] * (ing["quantidade_gramas"] / 100)
            total_calorias += cal
            self.lista_ingredientes.insert(tk.END, f'{ing["nome"]} - {ing["quantidade_gramas"]}g - {cal:.1f} kcal')
            nomes_ingredientes.append(ing["nome"])

        self.label_calorias.config(text=f"Total de calorias: {total_calorias:.1f} kcal")
        self.combo_ingredientes_prato["values"] = nomes_ingredientes



    def excluir_ingrediente_do_prato(self):
        if not self.id_prato_em_edicao:
            messagebox.showwarning("Aviso", "Selecione um prato primeiro.")
            return

        nome_ingrediente = self.combo_ingredientes_prato.get()
        if not nome_ingrediente:
            messagebox.showwarning("Aviso", "Selecione um ingrediente para excluir.")
            return

        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir '{nome_ingrediente}' deste prato?")
        if confirm:
            PratoController.remover_ingrediente(self.id_prato_em_edicao, nome_ingrediente)
            messagebox.showinfo("Sucesso", "Ingrediente removido do prato com sucesso.")
            self.atualizar_ingredientes_do_prato()

    def excluir_prato(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um prato para excluir.")
            return
        
        values = self.tree.item(item, "values")
        nome_prato = values[1]
        
        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o prato '{nome_prato}'?")
        if confirm:
            PratoController.excluir_prato(values[0])
            messagebox.showinfo("Sucesso", "Prato excluído com sucesso.")
            self.entry_nome.delete(0, tk.END)
            self.id_prato_em_edicao = None
            self.btn_salvar.config(text="Adicionar Prato")
            self.lista_ingredientes.delete(0, tk.END)
            self.label_calorias.config(text="")
            self.combo_ingredientes_prato["values"] = []
            self.atualizar_lista()
