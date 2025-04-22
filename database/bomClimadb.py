import sqlite3 as sql

# definindo nossa conexão com o banco de dados da loja
def db_connection():
    return sql.connect("bom_clima.db")



# função que executa ações com o banco de dados "bom_clima.db"
def querys(dbConnection,query:str):
    cursor=dbConnection.cursor()

    try:
        # executa nossa ação
        cursor.execute(query)
        # confirma operação com o db
        dbConnection.commit()

        # retorno de fim de operação
        return f"Operação bem sucedida"

    except sql.OperationalError as err:
        # retorno de fim de operação
        return f"ERROR: '{err}'"



# função que mostra todos os campos da tabela recebida
def show_all(dbConnection, table:str):
    # cursor para a conexão com banco de dados
    cursor=dbConnection.cursor()
    
    # variavel que recebe todos os dados retornados
    results=None

    query=f"""
SELECT *
FROM {table};
"""

    # busca todos os dados na tabela
    cursor.execute(query)

    # retorna dados como arrays para results
    return cursor.fetchall()