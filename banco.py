import sqlite3

class EstoqueDB:
    def __init__(self, db_name="estoque.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._criar_tabela()

    def _criar_tabela(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco REAL NOT NULL
        )''')
        self.conn.commit()

    def adicionar_produto(self, nome, quantidade, preco):  # <-- Nome corrigido
        self.cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
        self.conn.commit()

    def listar_produtos(self):
        self.cursor.execute("SELECT * FROM produtos")
        return self.cursor.fetchall()

    def atualizar_produto(self, id_produto, nome, quantidade, preco):
        self.cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?", (nome, quantidade, preco, id_produto))
        self.conn.commit()

    def deletar_produto(self, id_produto):
        self.cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
        self.conn.commit()

    def fechar_conexao(self):
        self.conn.close()
