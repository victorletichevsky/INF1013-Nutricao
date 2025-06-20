import tkinter as tk

def marcar_realizada():
    print("Refeição marcada como realizada!")

def voltar():
    print("Voltando à tela anterior...")

# Janela principal
root = tk.Tk()
root.title("2.2DetalhesRefeicao")
root.geometry("800x500")
root.configure(bg="white")

# Título
titulo = tk.Label(root, text="Detalhes da Refeição", font=("Arial", 16, "bold"), bg="white", fg="black")
titulo.pack(pady=20)

# Frame de conteúdo alinhado à esquerda
frame = tk.Frame(root, bg="white")
frame.pack(anchor="w", padx=60)

# Tipo de refeição
label_tipo = tk.Label(frame, text="Tipo de refeição: Almoço", font=("Arial", 12), bg="white", fg="black")
label_tipo.pack(anchor="w", pady=(5, 10))

# Botão "Marcar como realizada"
btn_realizada = tk.Button(frame, text="Marcar como realizada", font=("Arial", 11), bg="#C3E6CB", fg="black",
                          relief="solid", borderwidth=1, command=marcar_realizada)
btn_realizada.pack(anchor="w", pady=(0, 20))

# Prato selecionado
label_prato = tk.Label(frame, text="Prato selecionado: Frango grelhado com arroz", font=("Arial", 12), bg="white", fg="black")
label_prato.pack(anchor="w", pady=(0, 10))

# Calorias
label_calorias = tk.Label(frame, text="Calorias: 550 kcal", font=("Arial", 12), bg="white", fg="black")
label_calorias.pack(anchor="w")

# Botão Voltar no canto inferior esquerdo
btn_voltar = tk.Button(root, text="Voltar", font=("Arial", 11), bg="#D1ECF1", fg="black",
                       relief="solid", borderwidth=1, command=voltar)
btn_voltar.place(x=50, y=450)

root.mainloop()
