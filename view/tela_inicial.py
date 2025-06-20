import tkinter as tk
from tkinter import messagebox

def continuar():
    nome = entry_nome.get()
    refeicoes = entry_refeicoes.get()
    if not nome or not refeicoes:
        messagebox.showwarning("Campos obrigatórios", "Por favor, preencha todos os campos.")
        return
    print(f"Nome: {nome}")
    print(f"Refeições por dia: {refeicoes}")

# Janela principal
root = tk.Tk()
root.title("Tela Inicial")
root.geometry("400x300")
root.configure(bg="white")

# Frame central
frame = tk.Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Título
titulo = tk.Label(frame, text="Tela Inicial", font=("Arial", 16, "bold"), fg="black", bg="white")
titulo.pack(pady=(0, 20))

# Nome do usuário
label_nome = tk.Label(frame, text="Nome do usuário", font=("Arial", 12), fg="black", bg="white", anchor="w")
label_nome.pack(fill='x')
entry_nome = tk.Entry(frame, width=30, font=("Arial", 12))
entry_nome.pack(pady=(0, 10))

# Refeições por dia
label_refeicoes = tk.Label(frame, text="Refeições por dia", font=("Arial", 12), fg="black", bg="white", anchor="w")
label_refeicoes.pack(fill='x')
entry_refeicoes = tk.Entry(frame, width=30, font=("Arial", 12))
entry_refeicoes.pack(pady=(0, 20))

# Botão continuar
btn_continuar = tk.Button(frame, text="Continuar", font=("Arial", 12), command=continuar)
btn_continuar.pack()

root.mainloop()
