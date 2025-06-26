import tkinter as tk
from tkinter import ttk, messagebox
from controllers.ingrediente_controller import IngredienteController
from models.ingrediente_model import IngredienteModel

class TelaIngredientes(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")

        self.ingrediente_em_edicao = None

        tk.Label(self, text="Ingredientes", font=("Arial", 18), bg="white").pack(pady=10)

        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Calorias"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Calorias", text="Calorias (100g)")
        self.tree.column("ID", width=0, stretch=False)
        self.tree.pack(padx=10, pady=10, fill="x")

        self.tree.bind("<Double-1>", self.carregar_para_edicao)

        self.form_frame = tk.Frame(self, bg="white")
        self.form_frame.pack(pady=10)

        tk.Label(self.form_frame, text="Nome:", bg="white").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(self.form_frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.form_frame, text="Calorias (100g):", bg="white").grid(row=1, column=0, padx=5, pady=5)
        self.entry_calorias = tk.Entry(self.form_frame)
        self.entry_calorias.grid(row=1, column=1, padx=5, pady=5)

        self.btn_salvar = ttk.Button(self.form_frame, text="Adicionar", command=self.salvar)
        self.btn_salvar.grid(row=2, column=0, pady=10, padx=5)
        
        self.btn_excluir = ttk.Button(self.form_frame, text="Excluir", command=self.excluir_ingrediente)
        self.btn_excluir.grid(row=2, column=1, pady=10, padx=5)

        self.atualizar_lista()

    def atualizar_lista(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        ingredientes = IngredienteController.listar_ingredientes()
        for ing in ingredientes:
            self.tree.insert("", "end", values=(ing["id_ingrediente"], ing["nome"], ing["calorias_100g"]))

    def salvar(self):
        nome = self.entry_nome.get()
        calorias = self.entry_calorias.get()

        if not nome or not calorias:
            messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos.")
            return

        try:
            calorias = float(calorias)
        except ValueError:
            messagebox.showerror("Erro", "Calorias deve ser um número.")
            return

        if self.ingrediente_em_edicao:
            # Atualizar existente
            IngredienteController.editar_ingrediente(self.ingrediente_em_edicao, nome, calorias)
            messagebox.showinfo("Atualizado", "Ingrediente atualizado com sucesso.")
            self.ingrediente_em_edicao = None
            self.btn_salvar.config(text="Adicionar")
        else:
            # Novo ingrediente
            IngredienteController.adicionar_ingrediente(nome, calorias)
            messagebox.showinfo("Adicionado", "Ingrediente adicionado com sucesso.")

        self.entry_nome.delete(0, tk.END)
        self.entry_calorias.delete(0, tk.END)
        self.atualizar_lista()

    def carregar_para_edicao(self, event):
        item = self.tree.selection()
        if not item:
            return
        values = self.tree.item(item, "values")
        self.ingrediente_em_edicao = values[0]  # ID
        self.entry_nome.delete(0, tk.END)
        self.entry_calorias.delete(0, tk.END)
        self.entry_nome.insert(0, values[1])
        self.entry_calorias.insert(0, values[2])
        self.btn_salvar.config(text="Salvar")

    def excluir_ingrediente(self):
        item = self.tree.selection()
        if not item:
            messagebox.showwarning("Aviso", "Selecione um ingrediente para excluir.")
            return
        
        values = self.tree.item(item, "values")
        nome_ingrediente = values[1]
        
        confirm = messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir '{nome_ingrediente}'?")
        if confirm:
            IngredienteController.excluir_ingrediente(values[0])
            messagebox.showinfo("Sucesso", "Ingrediente excluído com sucesso.")
            self.entry_nome.delete(0, tk.END)
            self.entry_calorias.delete(0, tk.END)
            self.ingrediente_em_edicao = None
            self.btn_salvar.config(text="Adicionar")
            self.atualizar_lista()
