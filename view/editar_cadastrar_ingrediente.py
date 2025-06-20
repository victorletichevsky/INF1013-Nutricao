import tkinter as tk
from tkinter import messagebox
import os

# Força um tema amigável mesmo em modo escuro
os.environ['TK_THEME'] = 'clam'

def salvar_ingrediente():
    ingrediente = entry_ingrediente.get()
    calorias = entry_calorias.get()
    if not ingrediente or not calorias:
        messagebox.showwarning("Campos obrigatórios", "Preencha todos os campos!")
        return
    print(f"Ingrediente: {ingrediente}")
    print(f"Calorias (100g): {calorias}")

def voltar():
    print("Voltando para a tela anterior...")

# Janela principal
root = tk.Tk()
root.title("3.4EditarCadastrarIngrediente")
root.geometry("800x500")
root.configure(bg="white")

# Título
titulo = tk.Label(root, text="Editar/cadastrar ingrediente", font=("Arial", 16, "bold"), bg="white", fg="black")
titulo.pack(pady=20)

# Frame de conteúdo
frame = tk.Frame(root, bg="white")
frame.pack(anchor="w", padx=60)

# Ingrediente
label_ingrediente = tk.Label(frame, text="Ingrediente:", font=("Arial", 12), bg="white", fg="black")
label_ingrediente.grid(row=0, column=0, sticky="w", pady=5)
entry_ingrediente = tk.Entry(frame, font=("Arial", 12), width=30)
entry_ingrediente.grid(row=0, column=1, pady=5)

# Subtítulo
label_subtitulo = tk.Label(frame, text="Adicionar/editar ingrediente:", font=("Arial", 12), bg="white", fg="black")
label_subtitulo.grid(row=1, column=0, columnspan=2, sticky="w", pady=(10, 5))

# Calorias
label_calorias = tk.Label(frame, text="Calorias em 100g", font=("Arial", 12), bg="white", fg="black")
label_calorias.grid(row=2, column=0, sticky="w", pady=5)
entry_calorias = tk.Entry(frame, font=("Arial", 12), width=10)
entry_calorias.grid(row=2, column=1, sticky="w", pady=5)

# Botão Salvar
btn_salvar = tk.Button(frame, text="Salvar/cadastrar", font=("Arial", 11), bg="#C3E6CB", fg="black",
                       relief="solid", borderwidth=1, command=salvar_ingrediente)
btn_salvar.grid(row=3, column=0, columnspan=2, pady=20, sticky="w")

# Botão Voltar
btn_voltar = tk.Button(root, text="Voltar", font=("Arial", 11), bg="#D1ECF1", fg="black",
                       relief="solid", borderwidth=1, command=voltar)
btn_voltar.place(x=50, y=450)

root.mainloop()
