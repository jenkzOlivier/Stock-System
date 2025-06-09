import pytest
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

import sqlite3
from database_produto import ProdutoDatabase
from produto_model import ProdutoModel

@pytest.fixture
def setup_db():
    """Configura um banco de dados temporário para testes."""
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE produto (
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
    yield conn
    conn.close()

def test_criar_tabela(setup_db):
    """Verifica se a tabela é criada corretamente."""
    conn = setup_db
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='produto'")
    assert cursor.fetchone() is not None

def test_cadastrar_produto(setup_db):
    """Testa a inserção de um produto no banco de dados."""
    produto = ProdutoModel(nome="Produto Teste", marca="Marca Teste", descricao="Descrição Teste", referencia="Ref123", valor=100.0, quantidade=10)

    conn = setup_db
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO produto (nome, marca, descricao, referencia, valor, quantidade)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (produto.nome, produto.marca, produto.descricao, produto.referencia, produto.valor, produto.quantidade))

    conn.commit()
    cursor.execute("SELECT * FROM produto WHERE nome = ?", (produto.nome,))
    resultado = cursor.fetchone()
    
    assert resultado is not None
    assert resultado[1] == produto.nome

def test_listar_produtos(setup_db):
    """Verifica se os produtos podem ser listados corretamente."""
    conn = setup_db
    cursor = conn.cursor()

    produto_1 = ProdutoModel(nome="Produto 1", marca="Marca A", descricao="Descrição 1", referencia="Ref001", valor=50.0, quantidade=5)
    produto_2 = ProdutoModel(nome="Produto 2", marca="Marca B", descricao="Descrição 2", referencia="Ref002", valor=150.0, quantidade=2)

    cursor.execute('''
        INSERT INTO produto (nome, marca, descricao, referencia, valor, quantidade)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (produto_1.nome, produto_1.marca, produto_1.descricao, produto_1.referencia, produto_1.valor, produto_1.quantidade))
    
    cursor.execute('''
        INSERT INTO produto (nome, marca, descricao, referencia, valor, quantidade)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (produto_2.nome, produto_2.marca, produto_2.descricao, produto_2.referencia, produto_2.valor, produto_2.quantidade))

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM produto")
    resultado = cursor.fetchone()[0]
    
    assert resultado == 2

def test_excluir_produto(setup_db):
    """Testa a exclusão de um produto do banco de dados."""
    conn = setup_db
    cursor = conn.cursor()

    produto = ProdutoModel(nome="Produto Teste", marca="Marca Teste", descricao="Descrição Teste", referencia="Ref123", valor=100.0, quantidade=10)
    
    cursor.execute('''
        INSERT INTO produto (nome, marca, descricao, referencia, valor, quantidade)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (produto.nome, produto.marca, produto.descricao, produto.referencia, produto.valor, produto.quantidade))
    
    conn.commit()
    cursor.execute("DELETE FROM produto WHERE nome = ?", (produto.nome,))
    conn.commit()
    
    cursor.execute("SELECT * FROM produto WHERE nome = ?", (produto.nome,))
    resultado = cursor.fetchone()
    
    assert resultado is None

if __name__ == "__main__":
    pytest.main()
