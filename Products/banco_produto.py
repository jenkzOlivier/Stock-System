import sqlite3 as sql
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../database")) # criando acesso ao folder database
import bomClimadb as db

# arquivo de interação com banco de dados para tabela produto

def show_produtos():
    # conectando ao db
    conect=db.db_connection()
    
    # tenta interação com tabela para verificar existencia da tabela
    try:
        results=db.show_all(conect,"produtos")
        dados=[]

        for linha in results:
            dados.append({"id":linha[0], "nome":linha[1], "marca":linha[2], "descricao":linha[3], "referencia":linha[4], "valor":linha[5], "quantidade":linha[6]})

        return dados


    # caso tabela não exista a cria
    except sql.OperationalError:
    

        # linha responsavel por criar nossa tabela
        query="""
    CREATE TABLE produtos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        marca TEXT NOT NULL,
        descricao TEXT,
        referencia TEXT NOT NULL,
        valor REAL NOT NULL,
        quantidade INTEGER NOT NULL
    );
    """

        db.querys(conect,query)


def insert_produto(entrada:dict):
    conect=db.db_connection()

    # tratamento dos dados
    if entrada["descricao"] is None:
        query:str=f"""
        INSERT INTO produtos (nome, marca, referencia, valor, quantidade) VALUES 
        ('{entrada["nome"]}','{entrada["marca"]}','{entrada["referencia"]}',{entrada["valor"]},{entrada["quantidade"]})
        """

    else:
        query:str=f"""
        INSERT INTO produtos (nome, marca, descricao, referencia, valor, quantidade) VALUES 
        ('{entrada["nome"]}','{entrada["marca"]}','{entrada["descricao"]}','{entrada["referencia"]}',{entrada["valor"]},{entrada["quantidade"]})
        """

    # inserindo dados na tabela
    db.querys(conect,query)



def produto_filter(buscas:dict):
    conect=db.db_connection()
    cursor=conect.cursor()
    results:list=[]
    dados:list=[]
    query:str

    chaves:list=list(buscas.keys())
        

    if chaves[0]=="id":
        query=f"""
        SELECT * FROM produtos WHERE
        {chaves[0]} = {buscas[chaves[0]]};
        """

        cursor.execute(query)
        results=cursor.fetchall()
        for linha in results:
            dados.append({"id":linha[0], "nome":linha[1], "marca":linha[2], "descricao":linha[3], "referencia":linha[4], "valor":linha[5], "quantidade":linha[6]})
        
        return dados


    else:
        if chaves[0]=="valor" or chaves[0]=="quantidade":
            query=f"""
            SELECT * FROM produtos WHERE
            {chaves[0]} = {buscas[chaves[0]]};
            """

        else:
            query=f"""
            SELECT * FROM produtos WHERE
            {chaves[0]} = '{buscas[chaves[0]]}';
            """

    cursor.execute(query)
    results=cursor.fetchall()

    for linha in results:
        dados.append({"id":linha[0], "nome":linha[1], "marca":linha[2], "descricao":linha[3], "referencia":linha[4], "valor":linha[5], "quantidade":linha[6]})

    temp:list=[]

    for chave in chaves:
        for registro in dados:
            if registro[chave]==buscas[chave]:
                temp.append(registro)
            
        if temp==[]:return temp
        else:
            dados=temp
            temp=[]

    return dados


def edit_produto(id:int,campo:str,dado):
    conect=db.db_connection()

    # criando query para atualizar banco de dados
    try:
        query:str=f"""
        UPDATE produtos
        SET {campo}={int(dado)}
        WHERE id={id};
        """
    except ValueError:
        try:
            query:str=f"""
            UPDATE produtos
            SET {campo}={float(dado)}
            WHERE id={id};
            """

        except ValueError:
            query:str=f"""
            UPDATE produtos
            SET {campo}='{dado}'
            WHERE id={id};
            """

    # atualizando campos no banco de dados
    db.querys(conect,query)


# codigo não usado
# class EstoqueDB:
#     def __init__(self, db_name="estoque.db"):
#         self.conn = sqlite3.connect(db_name)
#         self.cursor = self.conn.cursor()
#         self._criar_tabela()

#     def _criar_tabela(self):
#         self.cursor.execute('''CREATE TABLE IF NOT EXISTS produtos (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             nome TEXT NOT NULL,
#             quantidade INTEGER NOT NULL,
#             preco REAL NOT NULL
#         )''')
#         self.conn.commit()

#     def adicionar_produto(self, nome, quantidade, preco): 
#         self.cursor.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)", (nome, quantidade, preco))
#         self.conn.commit()

#     def listar_produtos(self):
#         self.cursor.execute("SELECT * FROM produtos")
#         return self.cursor.fetchall()

#     def atualizar_produto(self, id_produto, nome, quantidade, preco):
#         self.cursor.execute("UPDATE produtos SET nome=?, quantidade=?, preco=? WHERE id=?", (nome, quantidade, preco, id_produto))
#         self.conn.commit()

#     def deletar_produto(self, id_produto):
#         self.cursor.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
#         self.conn.commit()

#     def fechar_conexao(self):
#         self.conn.close()
