import tkinter as tk
import threading
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    handlers=[logging.FileHandler("jiga_test.log"), logging.StreamHandler()]
)
logger = logging.getLogger("JIGA_TEST")

class TesteSequencialGUI:
    def __init__(self, master, test_report_db):
        self.master = master
        self.test_report_db = test_report_db
        self.master.attributes('-fullscreen', False)
        self.master.geometry("1000x700")  # Largura x Altura em pixels
        self.frame = tk.Frame(master, bg="black")
        self.frame.pack(fill="both", expand=True)

        self.status_label = tk.Label(self.frame, text="Aguardando inserção do produto...", font=("Arial", 32, "bold"), fg="white", bg="black")
        self.status_label.pack(pady=30)

        self._dut_present = False

        btn_frame = tk.Frame(self.frame, bg="black")
        btn_frame.pack(pady=8)
        
        inserir_btn = tk.Button(btn_frame, text="Inserir DUT", font=("Arial", 14), width=12,
                                command=lambda: self.set_dut(True), bg="#229933", fg="white")
        inserir_btn.pack(side="left", padx=15)
        
        remover_btn = tk.Button(btn_frame, text="Remover DUT", font=("Arial", 14), width=12,
                                command=lambda: self.set_dut(False), bg="#b81717", fg="white")
        remover_btn.pack(side="left", padx=15)

        # Define nomes fixos e funções dos testes
        self.test_names = [
            "Curto na alimentação",
            "Gravação Firmware",
            "Primeira Comunicação",
            "LED Test",
            "Testes Internos",
            "Consumo",
            "Comunicação Final",
            "Impressão Etiqueta"
        ]
        self.tests = [
            self.short_circuit_test,
            self.st_flash,
            self.first_communication,
            self.test_led,
            self.internal_tests,
            self.current_test,
            self.end_communication,
            self.print_label
        ]

        # Painel fixo dos testes
        self.test_labels = []
        self.status_labels = []
        test_panel = tk.Frame(self.frame, bg="black")
        test_panel.pack(pady=10)
        for name in self.test_names:
            row = tk.Frame(test_panel, bg="black")
            row.pack(anchor="w", pady=6)
            name_label = tk.Label(row, text=name, font=("Arial", 20), fg="white", bg="black", width=28, anchor="w")
            name_label.pack(side="left")
            status_label = tk.Label(row, text="", font=("Arial", 20, "bold"), fg="yellow", bg="black", width=18, anchor="w")
            status_label.pack(side="left")
            self.test_labels.append(name_label)
            self.status_labels.append(status_label)

        self.result_label = tk.Label(self.frame, text="", font=("Arial", 32, "bold"), fg="white", bg="black")
        self.result_label.pack(pady=30)
        self.reset_btn = tk.Button(self.frame, text="Sair", font=("Arial", 18), command=self.quit_app, bg="gray", fg="white")
        self.reset_btn.pack(side="bottom", pady=16)
        self.running = False
        self.restart()

    def restart(self):
        for status_label in self.status_labels:
            status_label.config(text="", fg="yellow")
        self.status_label.config(text="Aguardando inserção do produto...", fg="white", bg="black")
        self.result_label.config(text="", fg="white", bg="black")
        self.running = False
        self.master.after(400, self.wait_for_insert)

    def wait_for_insert(self):
        self.update_status("Aguardando inserção do produto...")
        if self.IsDUTPresent():
            self.start_teste()
        else:
            self.master.after(400, self.wait_for_insert)

    def start_teste(self):
        self.running = True
        self.dut_removed_during_test = False
        self.status_label.config(text="Executando testes...", fg="yellow", bg="black")
        # 2. Durante o teste, inicia o monitoramento da remoção indevida
        self.monitor_remocao_durante_teste()
        threading.Thread(target=self.run_tests, daemon=True).start()

    def monitor_remocao_durante_teste(self):
        # Detecta remoção indevida do DUT enquanto o teste está rodando
        if not self.IsDUTPresent():
            self.dut_removed_during_test = True
        else:
            # Só monitora se teste ainda está rodando
            if self.running:
                self.master.after(100, self.monitor_remocao_durante_teste)

    def run_tests(self):
        aprovado = True
        erro_msg = ""
        results = []
        for i, funcao in enumerate(self.tests):
            # Verifica a cada troca de teste se o DUT ainda está presente
            if not self.IsDUTPresent():
                aprovado = False
                erro_msg = "DUT removido durante o teste"
                # Sinaliza reprovação imediatamente
                self.set_status(i, "Reprovado: DUT removido", "red")
                results.append((self.test_names[i], "REPROVADO", "Removido durante o teste"))
                break
            self.set_status(i, "Executando...", "cyan")
            resultado, erro = funcao()
            if resultado == "OK":
                self.set_status(i, "Aprovado", "green")
                results.append((self.test_names[i], "APROVADO", ""))
            else:
                self.set_status(i, f"Reprovado: {erro or 'Erro'}", "red")
                results.append((self.test_names[i], "REPROVADO", erro or "Erro"))
                aprovado = False
                erro_msg = erro or "Falha desconhecida"
                break
            time.sleep(0.3)
        self.running = False
        self.salvar_relatorio(aprovado, results)
        self.fim_teste(aprovado, erro_msg)

    def set_status(self, idx, txt, color):
        self.status_labels[idx].config(text=txt, fg=color)
        self.master.update()

    def fim_teste(self, aprovado, erro_msg):
        if aprovado:
            self.status_label.config(text="PRODUTO APROVADO! Remova o produto.", fg="black", bg="green")
            self.result_label.config(text="APROVADO", fg="green", bg="black")
        else:
            if erro_msg == "DUT removido durante o teste":
                self.status_label.config(text="DUT REMOVIDO DURANTE O TESTE!\nReinicie o processo.", fg="white", bg="red")
                self.result_label.config(text="REPROVADO\nRemovido durante teste", fg="red", bg="black")
            else:
                self.status_label.config(text="PRODUTO REPROVADO! Remova o produto.", fg="white", bg="red")
                self.result_label.config(text=f"REPROVADO\n{erro_msg}", fg="red", bg="black")
        # 3. Após teste, monitora a remoção para só então reiniciar
        self.master.after(200, self.wait_for_remove)

    def wait_for_remove(self):
        self.update_status("Aguardando remoção do produto...")
        if not self.IsDUTPresent():
            self.restart()
        else:
            self.master.after(400, self.wait_for_remove)

    def update_status(self, msg=None):
        if msg:
            self.status_label.config(text=msg)
        self.master.update()

    def salvar_relatorio(self, aprovado, results):
        try:
            status_final = "APROVADO" if aprovado else "REPROVADO"
            test_data = {
                "resultado": status_final,
                "etapas": results
            }
            self.test_report_db.salvar(test_data)
            logger.info("Relatório de teste salvo no banco de dados.")
        except Exception as e:
            logger.error(f"Erro ao salvar relatório: {e}")

    def quit_app(self):
        self.master.destroy()

    def set_dut(self, val: bool):
        self._dut_present = val

    # ----------- Simulações (troque por suas funções reais) ----------------
    def IsDUTPresent(self):
        return self._dut_present

    def short_circuit_test(self):
        # Simulação de teste real
        #return ("NOK", "Current OK: 2.5A")    
        return ("OK", "Current OK: 0.5A")

    def st_flash(self):
        time.sleep(1)  # Simula o tempo de gravação        
        return ("OK", None)

    def first_communication(self):
        time.sleep(3)  # Simula o tempo de gravação     
        return ("OK", None)

    def test_led(self):
        time.sleep(1)  # Simula o tempo de gravação     
        return ("OK", None)

    def internal_tests(self):
        time.sleep(5)  # Simula o tempo de gravação
        #return ("NOK", "ACC not response")    
        return ("OK", None)

    def current_test(self):
        time.sleep(2)  # Simula o tempo de gravação 
        #return ("NOK", "Current OK: 60.3 uA")    
        return ("OK", "Current OK: 2.2 uA")

    def end_communication(self):
        time.sleep(1)  # Simula o tempo de gravação     
        return ("OK", None)

    def print_label(self):
        time.sleep(2)  # Simula o tempo de gravação     
        return ("OK", None)


class DummyTestReportDB:
    def salvar(self, test_data):
        print("Relatório salvo:", test_data)


if __name__ == "__main__":
    root = tk.Tk()
    db = DummyTestReportDB()  # Troque pelo seu objeto real
    app = TesteSequencialGUI(root, db)
    root.mainloop()
