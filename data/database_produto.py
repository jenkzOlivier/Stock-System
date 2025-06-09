import sqlite3
from produto_model import ProdutoModel




class ProdutoDatabase:
    @staticmethod
    def conectar(nome_do_banco: str = "produtos.db"):
        #se voce quiser esecificar um banco lembre de fazer polimorfismo no metodo criar_tabela abaixo
        #para poder fazer as consultaas do jeito que quiser, essa clase NÃO PODE SER ALTERADA.
        if nome_do_banco is not None:
            return sqlite3.connect(nome_do_banco)
        return sqlite3.connect('produtos.db')



    @staticmethod
    def criar_tabela():
        conn = ProdutoDatabase.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS produto (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                marca TEXT,
                descricao TEXT,
                referencia TEXT,
                valor REAL,
                quantidade INTEGER
            )
        ''')
        conn.commit()
        conn.close()



    @staticmethod
    def cadastrar_produto(produto: ProdutoModel):
        conn = ProdutoDatabase.conectar()
        cursor = conn.cursor()
        cursor.execute('''
         INSERT INTO produto (nome, marca, descricao, referencia, valor, quantidade)
         VALUES (?, ?, ?, ?, ?, ?)
     ''', (produto.nome, produto.marca, produto.descricao, produto.referencia, produto.valor, produto.quantidade))
        conn.commit()
        last_id = cursor.lastrowid
        conn.close()
        return last_id




    @staticmethod
    def listar_produtos():
        conn = ProdutoDatabase.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produto')
        produtos = cursor.fetchall()
        conn.close()
        return [ProdutoModel(id=row[0], nome=row[1], marca=row[2], descricao=row[3], referencia=row[4], valor=row[5], quantidade=row[6]) for row in produtos]


    @staticmethod
    def editar_produto(produto):
        conn = ProdutoDatabase.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE produto
            SET nome = ?, marca = ?, descricao = ?, referencia = ?, valor = ?, quantidade = ?
            WHERE id = ?
        ''', (produto.nome, produto.marca, produto.descricao, produto.referencia, produto.valor, produto.quantidade, produto.id))
        conn.commit()
        conn.close()


    @staticmethod
    def deletar_produto(id):
        conn = ProdutoDatabase.conectar()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM produto WHERE id = ?', (id,))
        conn.commit()
        conn.close()


    @staticmethod
    def buscar_produto_por_id(id):
        conn = ProdutoDatabase.conectar()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM produto WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return ProdutoModel(id=row[0], nome=row[1], marca=row[2], descricao=row[3], referencia=row[4], valor=row[5], quantidade=row[6])
        return None
