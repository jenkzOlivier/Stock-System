import bcrypt
import os
import sys
import sqlite3 as sql
sys.path.append(os.path.join(os.path.dirname(__file__),"../database")) # criando acesso ao folder database
import bomClimadb as db

# função que verifica se a tabela de usuarios esta no database
def check_funcionario_table():
    # conectando ao db
    conect=db.db_connection()
    
    try:
        results:list=db.show_all(conect,"funcionarios")
        
        # verificando se existem credenciais dos funcionarios no banco de dados
        temp:int=0
        for i in results:
            temp+=1

        # retorno de erro de não existencia de credenciais de funcionarios
        if temp==1:return 0

        elif temp==[]:
            # criando usuario para suporte tecnico
            garante_suporte()
            return 0

        # retorno comum autorizando funcionamento 
        else:return 1

    # caso não exista a tabela
    except sql.OperationalError:
        query:str=f"""
        CREATE TABLE funcionarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        funcionario TEXT NOT NULL,
        senha TEXT NOT NULL,
        acesso TEXT NOT NULL,
        estado TEXT NOT NULL
        );
        """

        db.querys(conect,query)

        # criando usuario para suporte tecnico junto a criação do banco
        garante_suporte()
        
        return 0



def garante_suporte():
    conect=db.db_connection()

    # senha do suporte
    senha_hash=hash_password("suporte")

    # inserindo usuario suporte ao banco de dados
    query:str=f"""
    INSERT INTO funcionarios (funcionario,senha,acesso,estado) VALUES
    ('suporte','{senha_hash}','suporte','ATIVO')
    """

    db.querys(conect,query)



# função para hash da senha
def hash_password(senha:str):
    return bcrypt.hashpw(senha.encode(),bcrypt.gensalt()).decode()



# função para descriptar senha
def verify_password(senha:str,hashed_password):
    return bcrypt.checkpw(senha.encode(),hashed_password.encode())



def insert_funcionario(entrada:dict):
    conect=db.db_connection()

    senha_hash=hash_password(entrada["senha"])

    query:str=f"""
    INSERT INTO funcionarios (funcionario,senha,acesso,estado) VALUES
    ('{entrada["funcionario"]}','{senha_hash}','{entrada["acesso"]}','ATIVO')
    """

    db.querys(conect,query)



# função para retornar funcionarios salvos no db para login
def login_funcionario(funcionario:str,senha:str):
    conect=db.db_connection()
    cursor=conect.cursor()

    query:str=f"""SELECT * FROM funcionarios WHERE funcionario='{funcionario}';"""
    cursor.execute(query)

    temp:list=cursor.fetchall()

    results:list=[]
    for i in temp:
        if i[4]=="ATIVO":
            results.append({"funcionario":i[1],"senha":i[2],"acesso":i[3]})

    if results==[]:return {"acao":0}
    else:
        for user in results:
            if verify_password(senha,user["senha"]):
                # ação para acesso ao sistema retornando mensagem de sucesso
                return {"acao":1,"acesso":user["acesso"],"funcionario":user["funcionario"]}

            else:return {"acao":0}



def cadastro_acesso(nivel:str):

    if nivel=="admin": return ["admin","editor"]

    elif nivel=="suporte": return ["suporte","admin","editor"]

    else: return []


def edit_funcionario(id:int,campo:str,dado:str):
    conect=db.db_connection()

    query:str=f"""
    UPDATE funcionarios
    SET {campo}='{dado}'
    WHERE id={id};
    """

    db.querys(conect,query)
