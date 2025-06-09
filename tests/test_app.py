import pytest
import sys
import os
import uuid

# Caminhos
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

# Importa o app verdadeiro
from app import app
import database_usuario
from database_produto import ProdutoDatabase
from produto_model import ProdutoModel
from services import password_hashing

# Fixture client correto
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_criar_tabela():
    assert database_usuario.criar_tabela() is None  # Verifica se a função executa corretamente

def test_adicionar_usuario():
    usuario = f"teste_{uuid.uuid4().hex[:8]}"
    senha = "senha_teste"
    acesso = "admin"
    senha_hash = password_hashing.hash_password(senha)

    # Certifique-se de que o usuário não existe
    existente = database_usuario.buscar_usuario(usuario)
    if existente:
        database_usuario.excluir_usuario(existente[1])  # ou ID se necessário

    database_usuario.adicionar_usuario(usuario, senha_hash, acesso)
    resultado = database_usuario.buscar_usuario(usuario)
    assert resultado is not None
    assert resultado[0] == usuario

def test_login_usuario(client):
    usuario = f"login_{uuid.uuid4().hex[:8]}"
    senha = "senha_teste"
    senha_hash = password_hashing.hash_password(senha)

    # Adiciona usuário
    database_usuario.criar_tabela()
    database_usuario.adicionar_usuario(usuario, senha_hash, "admin")

    resposta = client.post("/login", data={"usuario": usuario, "senha": senha})
    assert resposta.status_code in [200, 302]

def test_cadastrar_produto():
    produto = ProdutoModel(
        nome=f"Produto Teste {uuid.uuid4().hex[:4]}",
        marca="Marca Teste",
        descricao="Descrição Teste",
        referencia="Ref123",
        valor=100.0,
        quantidade=10
    )

    produto_id = ProdutoDatabase.cadastrar_produto(produto)
    assert produto_id is not None

    produto_salvo = ProdutoDatabase.buscar_produto_por_id(produto_id)
    assert produto_salvo is not None
    assert produto_salvo.nome == produto.nome

def test_excluir_produto():
    produto = ProdutoModel(
        nome="Produto para Excluir",
        marca="Marca",
        descricao="Descrição",
        referencia="RefDel",
        valor=10.0,
        quantidade=1
    )
    produto_id = ProdutoDatabase.cadastrar_produto(produto)

    ProdutoDatabase.deletar_produto(produto_id)
    produto_salvo = ProdutoDatabase.buscar_produto_por_id(produto_id)
    assert produto_salvo is None

if __name__ == "__main__":
    pytest.main()
