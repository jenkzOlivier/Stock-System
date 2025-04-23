import sqlite3
import bcrypt
import os

# Caminho do banco de dados
db_file = "loginDatabase.db"

# Conectar ao banco de dados SQLite
def get_connection():
    return sqlite3.connect(db_file)

# Criar a tabela de usuários (caso não exista)
def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            nivel_acesso TEXT NOT NULL
        )
        """)
        conn.commit()

# Função para hash de senha
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Função para verificar senha
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Função para criar o admin se não existir
def ensure_admin():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = ?", ("admin",))
        if cursor.fetchone() is None:
            senha_hash = hash_password("admin")
            cursor.execute("INSERT INTO usuarios (nome, senha, nivel_acesso) VALUES (?, ?, ?)", 
                           ("admin", senha_hash, "admin"))
            conn.commit()

# Chamar a função para inicializar o banco e garantir que o admin exista
init_db()
ensure_admin()



ACCESS_LEVELS = {
    "admin": "Administrador",
    "editor": "Editor",
    "viewer": "Visualizador"
}
