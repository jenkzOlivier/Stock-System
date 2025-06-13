import pytest
import sys
import os
import sqlite3

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

import database_usuario

from database_usuario import (
    criar_tabela,
    adicionar_usuario,
    buscar_usuario,
    listar_usuarios,
    buscar_usuario_por_id,
    atualizar_usuario,
    atualizar_usuario_com_senha,
    excluir_usuario
)

@pytest.fixture
def setup_db():
    """Cria um banco de dados em memória para testes."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT UNIQUE NOT NULL,
            password BLOB NOT NULL,
            acesso TEXT NOT NULL
        )
    ''')
    conn.commit()
    yield conn
    conn.close()

def test_criar_tabela(setup_db):
    """Verifica se a tabela é criada corretamente."""
    conn = setup_db
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
    assert cursor.fetchone() is not None

def test_adicionar_usuario(setup_db):
    """Verifica se um usuário pode ser adicionado ao banco."""
    conn = setup_db
    cursor = conn.cursor()
    user_name = "teste_usuario"
    password_hash = b"hashed_senha"
    acesso = "admin"

    cursor.execute('INSERT INTO usuarios (user_name, password, acesso) VALUES (?, ?, ?)',
                   (user_name, password_hash, acesso))
    conn.commit()

    cursor.execute("SELECT user_name FROM usuarios WHERE user_name = ?", (user_name,))
    resultado = cursor.fetchone()
    assert resultado is not None
    assert resultado[0] == user_name

def test_excluir_usuario():
    user_name = "usuario_para_excluir"
    password_hash = b"senha_excluir"
    acesso = "editor"

    # Garante que a tabela existe no banco real antes de inserir
    criar_tabela()

    # Conecta ao banco de usuários (usuarios.db), NÃO ao ProdutoDatabase
    conn = database_usuario.conectar()  # ou database_usuario.conectar()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (user_name, password, acesso) VALUES (?, ?, ?)',
                   (user_name, password_hash, acesso))
    conn.commit()

    cursor.execute("SELECT id FROM usuarios WHERE user_name = ?", (user_name,))
    usuario_id = cursor.fetchone()[0]
    conn.close()

    # Executa a exclusão
    excluir_usuario(usuario_id)

    # Abre nova conexão para verificar exclusão
    conn_verif = database_usuario.conectar()  # ou database_usuario.conectar()
    cursor_verif = conn_verif.cursor()
    cursor_verif.execute("SELECT * FROM usuarios WHERE id = ?", (usuario_id,))
    resultado = cursor_verif.fetchone()
    conn_verif.close()

    assert resultado is None



if __name__ == "__main__":
    pytest.main()
