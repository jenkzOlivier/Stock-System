# database.py
import sqlite3


def conectar():
    return sqlite3.connect('usuarios.db')


def criar_tabela():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            acesso TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_usuario(user_name, password_hash, acesso):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (user_name, password, acesso) VALUES (?, ?, ?)',
                   (user_name, password_hash, acesso))
    conn.commit()
    conn.close()

def buscar_usuario(user_name):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_name, password, acesso FROM usuarios WHERE user_name = ?', (user_name,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado  # retorna (user_name, hashed_password_bytes, acesso)


##### CODIGO ESPECIFICO PARA ROTAS DE CRUD NO FRONTEND####
def listar_usuarios():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_name, acesso FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def buscar_usuario_por_id(id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, user_name, acesso FROM usuarios WHERE id = ?', (id,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario

def atualizar_usuario(id, user_name, acesso):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET user_name = ?, acesso = ? WHERE id = ?', (user_name, acesso, id))
    conn.commit()
    conn.close()

def atualizar_usuario_com_senha(id, user_name, password_hash, acesso):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE usuarios
        SET user_name = ?, password = ?, acesso = ?
        WHERE id = ?
    ''', (user_name, password_hash, acesso, id))
    conn.commit()
    conn.close()

def excluir_usuario(id):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
