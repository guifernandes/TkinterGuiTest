import tkinter as tk  # import the Tkinter module

def on_button_click():
    """Callback when the button is clicked."""
    label.config(text="Você clicou no botão!")

root = tk.Tk()
root.title("Exemplo de Evento")
root.geometry("300x150")

label = tk.Label(root, text="Pressione o botão abaixo.")
button = tk.Button(root, text="Clique aqui", command=on_button_click)
# note: 'command' links the button to our callback

label.pack(pady=10)
button.pack()

root.mainloop()
