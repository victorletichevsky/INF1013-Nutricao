import tkinter as tk
from tkinter import ttk, messagebox

# Dados simulados
ingredientes_atuais = [
    ("Aveia", "50g"),
    ("Banana", "50g"),
    ("Mel", "10g")
]
opcoes_ingredientes = ["Banana", "Aveia", "Mel", "Frango", "Arroz"]

# Ações
def remover_ingrediente(index):
    print(f"Removido: {ingredientes_atuais[index][0]}")

def adicionar_ingrediente():
    ingr = combo_ingrediente.get()
    qtd = entry_quantidade.get()
    if ingr and qtd:
        print(f"Adicionado: {ingr} - {qtd}")
    else:
        messagebox.showwarning("Campos vazios", "Selecione um ingrediente e insira uma quantidade.")

def salvar_prato():
    print("Prato salvo.")

def voltar():
    print("Voltando...")

# Janela principal
root = tk.Tk()
root.title("3.2EditarCadastrarPrato")
root.geometry("900x550")
root.configure(bg="white")

# Estilo visual do Combobox forçado para fundo branco
style = ttk.Style()
style.theme_use("default")
style.configure("TCombobox",
                fieldbackground="white",
                background="white",
                foreground="black")

# Título
titulo = tk.Label(root, text="Editar/cadastrar prato", font=("Arial", 16, "bold"), bg="white", fg="black")
titulo.pack(pady=20)

# Frame principal
frame = tk.Frame(root, bg="white")
frame.pack(anchor="w", padx=60)

# Nome do prato
tk.Label(frame, text="Prato:", font=("Arial", 12), bg="white", fg="black").grid(row=0, column=0, sticky="w")
entry_prato = tk.Entry(frame, font=("Arial", 12), width=30, bg="white", fg="black")
entry_prato.insert(0, "Panqueca de Aveia")
entry_prato.grid(row=0, column=1, columnspan=2, pady=5, sticky="w")

# Ingredientes atuais
tk.Label(frame, text="\nIngredientes atuais:", font=("Arial", 12), bg="white", fg="black").grid(row=1, column=0, sticky="nw")

for i, (nome, qtd) in enumerate(ingredientes_atuais):
    tk.Label(frame, text=f"- {nome} ({qtd})", font=("Arial", 11), bg="white", fg="black").grid(row=2+i, column=0, sticky="w")
    btn_remover = tk.Button(frame, text="Remover", font=("Arial", 10), bg="#F8D7DA", fg="black",
                            relief="solid", borderwidth=1, command=lambda idx=i: remover_ingrediente(idx))
    btn_remover.grid(row=2+i, column=1, sticky="w", padx=10, pady=2)

# Adicionar novo ingrediente
linha_adicionar = 2 + len(ingredientes_atuais) + 1
tk.Label(frame, text="\nAdicionar novo ingrediente:", font=("Arial", 12), bg="white", fg="black").grid(row=linha_adicionar, column=0, sticky="w", pady=(10, 0))

tk.Label(frame, text="Ingrediente:", font=("Arial", 11), bg="white", fg="black").grid(row=linha_adicionar+1, column=0, sticky="w")
combo_ingrediente = ttk.Combobox(frame, values=opcoes_ingredientes, width=27)
combo_ingrediente.set("Selecione um ingrediente...")
combo_ingrediente.grid(row=linha_adicionar+1, column=1, columnspan=2, pady=2, sticky="w")

tk.Label(frame, text="Quantidade:", font=("Arial", 11), bg="white", fg="black").grid(row=linha_adicionar+2, column=0, sticky="w")
entry_quantidade = tk.Entry(frame, font=("Arial", 11), width=20, bg="white", fg="black")
entry_quantidade.insert(0, "em gramas")
entry_quantidade.grid(row=linha_adicionar+2, column=1, pady=2, sticky="w")

btn_adicionar = tk.Button(frame, text="Adicionar", font=("Arial", 11), bg="#D1ECF1", fg="black",
                          relief="solid", borderwidth=1, command=adicionar_ingrediente)
btn_adicionar.grid(row=linha_adicionar+3, column=0, pady=15, sticky="w")

# Botão salvar
btn_salvar = tk.Button(frame, text="Salvar/cadastrar", font=("Arial", 11), bg="#C3E6CB", fg="black",
                       relief="solid", borderwidth=1, command=salvar_prato)
btn_salvar.grid(row=linha_adicionar+4, column=0, pady=15, sticky="w")

# Botão voltar
btn_voltar = tk.Button(root, text="Voltar", font=("Arial", 11), bg="#D1ECF1", fg="black",
                       relief="solid", borderwidth=1, command=voltar)
btn_voltar.place(x=50, y=500)

root.mainloop()
