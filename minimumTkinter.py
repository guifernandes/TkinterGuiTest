import tkinter as tk  # import the Tkinter module

# 1. Criar a janela principal
root = tk.Tk()                  
root.title("Minha Primeira GUI")  # Set window title
root.geometry("300x200")          # Set default size (width x height)

# 2. Criar widgets
label = tk.Label(root, text="Olá, Tkinter!")  
button = tk.Button(root, text="Clique em mim")

# 3. Posicionar widgets na janela
label.pack(pady=10)   # pack with some vertical padding
button.pack()

# 4. Entrar no loop de eventos
root.mainloop()

# tk.Tk(): cria a janela raiz (root).

# Widgets (Label, Button, etc.) são criados passando como primeiro argumento a janela/pai (root).

# pack, grid ou place definem como o widget será posicionado. Aqui usamos pack por simplicidade.

# mainloop() inicia o loop que aguarda ações do usuário (cliques, teclado, etc.).