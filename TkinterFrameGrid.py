import tkinter as tk

root = tk.Tk()
root.title("Grid e Frames")
root.geometry("400x200")

# Frame superior
top_frame = tk.Frame(root)
tk.Label(top_frame, text="Nome:").grid(row=0, column=0, sticky="e")
tk.Entry(top_frame).grid(row=0, column=1, padx=5)

tk.Label(top_frame, text="Idade:").grid(row=1, column=0, sticky="e")
tk.Entry(top_frame).grid(row=1, column=1, padx=5)

top_frame.pack(pady=10)

# Frame inferior com botões
bottom_frame = tk.Frame(root)
tk.Button(bottom_frame, text="Salvar").grid(row=0, column=0, padx=10)
tk.Button(bottom_frame, text="Cancelar", command=root.quit).grid(row=0, column=1, padx=10)
bottom_frame.pack(pady=10)

root.mainloop()

# grid(row, column) facilita distribuir widgets em linhas e colunas.

# sticky, padx, pady ajudam a alinhar e espaçar.