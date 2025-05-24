import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("App Orientado a Objetos")
        self.geometry("300x150")
        self.build_ui()

    def build_ui(self):
        self.label = ttk.Label(self, text="Bem-vindo!")
        self.button = ttk.Button(self, text="Clique", command=self.on_click)
        self.label.pack(pady=10)
        self.button.pack()

    def on_click(self):
        self.label.config(text="Você clicou :)")

if __name__ == "__main__":
    app = App()
    app.mainloop()

# Este é um exemplo simples de uma aplicação GUI usando Tkinter.
# A classe App herda de tk.Tk e cria uma janela com um rótulo e um botão.
# Quando o botão é clicado, o texto do rótulo muda.
# O código é organizado em uma classe, seguindo o paradigma de programação orientada a objetos.
# O uso de classes permite encapsular a lógica da aplicação e facilita a manutenção e expansão do código.
# O Tkinter é uma biblioteca padrão do Python para criar interfaces gráficas.
# O código é executado dentro de um bloco if __name__ == "__main__" para garantir que a aplicação
# seja executada apenas quando o script é chamado diretamente, e não quando importado como um módulo.
# O método mainloop() inicia o loop principal da aplicação, permitindo que a interface gráfica responda a eventos.
# O método build_ui() é responsável por construir a interface do usuário, criando os widgets e organizando-os na janela.
# O método on_click() é chamado quando o botão é clicado, alterando o texto do rótulo.
# O uso de ttk (Themed Tkinter) permite criar interfaces mais modernas e atraentes.
# O layout é gerenciado pelo método pack(), que organiza os widgets verticalmente.
# O uso de padding (pady) adiciona espaço ao redor dos widgets, melhorando a aparência da interface.
# O código é simples e direto, ideal para iniciantes que desejam aprender sobre programação orientada a objetos
# e interfaces gráficas em Python. A estrutura do código é clara e fácil de entender, facilitando a leitura e manutenção.