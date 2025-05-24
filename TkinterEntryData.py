import tkinter as tk

def show_entry_text():
    user_input = entry.get()  # read text from Entry widget
    label.config(text=f"Você digitou: {user_input}")

root = tk.Tk()
root.title("Entry Example")
root.geometry("350x180")

label = tk.Label(root, text="Digite algo e pressione OK:")
entry = tk.Entry(root, width=30)
button = tk.Button(root, text="OK", command=show_entry_text)

label.pack(pady=(10,5))
entry.pack(pady=5)
button.pack(pady=5)

root.mainloop()

# O parâmetro command do Button recebe uma função Python (sem parênteses!) que será executada ao clicar.