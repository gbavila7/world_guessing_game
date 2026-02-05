import tkinter as tk
from tkinter import ttk, messagebox
import math
from datetime import datetime

from banco_dados import BancoDados
from servico_api import ServicoAPI


class JogoApp(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("🌍 World Guessing Game")
        self.geometry("600x500")

        self.db = BancoDados()
        self.api = ServicoAPI()

        self.inicio = None
        self.pais_atual = None

        self.criar_widgets()
        self.nova_rodada()

    # ======================
    # Interface
    # ======================
    def criar_widgets(self):

        tk.Label(self, text="Capital:", font=("Arial", 14)).pack(pady=5)

        self.lbl_dica = tk.Label(self, font=("Arial", 18, "bold"))
        self.lbl_dica.pack(pady=5)

        tk.Label(self, text="Seu nome:").pack()
        self.entry_nome = tk.Entry(self)
        self.entry_nome.pack()

        tk.Label(self, text="Palpite do país:").pack()
        self.entry_palpite = tk.Entry(self)
        self.entry_palpite.pack(pady=5)

        tk.Button(self, text="Chutar", command=self.processar_palpite)\
            .pack(pady=10)

        # ===== Treeview Ranking =====
        colunas = ("Jogador", "Pontos", "Data")

        self.tree = ttk.Treeview(self, columns=colunas, show="headings")

        for c in colunas:
            self.tree.heading(c, text=c)
            self.tree.column(c, anchor="center")

        self.tree.pack(expand=True, fill="both", pady=10)

        self.atualizar_ranking()

    # ======================
    # Lógica do jogo
    # ======================
    def nova_rodada(self):
        self.pais_atual = self.api.obter_pais_aleatorio()

        self.lbl_dica.config(text=self.pais_atual["capital"])

        self.entry_palpite.delete(0, tk.END)

        self.inicio = datetime.now()

    def calcular_pontos(self, tempo):
        base = math.floor(1000 / max(tempo, 1))

        bonus = 1 + (1 / math.log(self.pais_atual["populacao"] + 10))

        return int(base * bonus)

    def processar_palpite(self):
        nome_jogador = self.entry_nome.get()
        palpite = self.entry_palpite.get()

        if not nome_jogador or not palpite:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return

        fim = datetime.now()
        tempo = (fim - self.inicio).total_seconds()

        if palpite.lower() == self.pais_atual["nome"].lower():

            pontos = self.calcular_pontos(tempo)

            messagebox.showinfo(
                "Acertou!",
                f"Você ganhou {pontos} pontos!"
            )

            self.db.salvar(nome_jogador, pontos)

            self.atualizar_ranking()
            self.nova_rodada()

        else:
            messagebox.showerror(
                "Errado!",
                f"O país correto era {self.pais_atual['nome']}"
            )
            self.nova_rodada()

    # ======================
    # Ranking
    # ======================
    def atualizar_ranking(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        dados = self.db.listar_top5()

        for linha in dados:
            self.tree.insert("", tk.END, values=linha)
