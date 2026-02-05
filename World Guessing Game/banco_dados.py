import sqlite3
from datetime import datetime


class BancoDados:
    def __init__(self, nome_db="ranking.db"):
        self.conn = sqlite3.connect(nome_db)
        self.criar_tabela()

    def criar_tabela(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ranking(
                jogador TEXT,
                pontuacao INTEGER,
                data_hora TEXT
            )
        """)
        self.conn.commit()

    def salvar(self, jogador, pontuacao):
        cursor = self.conn.cursor()
        data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        cursor.execute(
            "INSERT INTO ranking VALUES (?, ?, ?)",
            (jogador, pontuacao, data)
        )
        self.conn.commit()

    def listar_top5(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT jogador, pontuacao, data_hora
            FROM ranking
            ORDER BY pontuacao DESC
            LIMIT 5
        """)

        return cursor.fetchall()
