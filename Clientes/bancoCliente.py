import sqlite3 as sql
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../database")) # criando acesso ao folder database
import bomClimadb as db

# arquivo com interação com o banco db com a tabela clientes

def show_clientes():
    # conectando ao db
    conect=db.db_connection()
    
    # tenta interação com tabela para verificar existencia da tabela
    try:
        results=db.show_all(conect,"clientes")
        dados=[]

        # modificar com dados da tabela
        for linha in results:
            dados.append({"id":linha[0], "nome":linha[1], "endereco":linha[2], "telefone":linha[3]})

        return dados


    # caso tabela não exista a cria
    except sql.OperationalError:
    

        # linha responsavel por criar nossa tabela
        query="""
        CREATE TABLE clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            telefone TEXT NOT NULL
        );
    """

        db.querys(conect,query)


def insert_cliente(entrada:dict):
    conect=db.db_connection()

    query:str=f"""
    INSERT INTO clientes (nome, endereco, telefone) VALUES
    ('{entrada["nome"]}', '{entrada["endereco"]}', '{entrada["telefone"]}')
    """

    db.querys(conect,query)

def cliente_filter(buscas:dict):
    conect=db.db_connection()
    cursor=conect.cursor()
    results:list=[]
    dados:list=[]
    temp:list=[]
    query:str

    chaves:list=list(buscas.keys())

    if chaves[0]=="id":
        query=f"""
        SELECT * FROM clientes WHERE
        {chaves[0]}={buscas[chaves[0]]}
        """

    else:
        query=f"""
        SELECT * FROM produtos WHERE
        {chaves[0]} = '{buscas[chaves[0]]}';
        """

    cursor.execute(query)
    results=cursor.fetchall()

    for linha in results:
        dados.append({"id":linha[0], "nome":linha[1], "endereco":linha[2], "telefone":linha[3]})

    for chave in chaves:
        for registro in dados:
            if registro[chave]==buscas[chave]:temp.append(registro)
            else:pass

        if temp==[]:return temp
        else:
            dados=temp
            temp=[]

    return dados


def edit_cliente(id:int,campo:str,dado:str):
    conect=db.db_connection()

    # query para atualização da tabela cliente
    query:str=f"""
    UPDATE produtos
    SET {campo}='{dado}'
    WHERE id={id};
    """

    db.querys(conect,query)
