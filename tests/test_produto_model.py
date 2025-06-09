import pytest
import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

from produto_model import ProdutoModel
from database_produto import ProdutoDatabase  # Supondo que haja um banco de dados para produtos

@pytest.fixture
def produto_exemplo():
    return ProdutoModel(
        nome="Produto Teste",
        marca="Marca Teste",
        descricao="Descrição Teste",
        referencia="Ref123",
        valor=100.0,
        quantidade=10
    )

def test_criacao_produto(produto_exemplo):
    # Como o id não existe ainda, só testa os outros campos
    assert produto_exemplo.nome == "Produto Teste"
    assert produto_exemplo.marca == "Marca Teste"
    assert produto_exemplo.descricao == "Descrição Teste"
    assert produto_exemplo.referencia == "Ref123"
    assert produto_exemplo.valor == 100.0
    assert produto_exemplo.quantidade == 10

def test_cadastrar_produto(produto_exemplo):
    produto_id = ProdutoDatabase.cadastrar_produto(produto_exemplo)
    produto_exemplo.id = produto_id  # atualiza o id no objeto para buscar depois

    produto_salvo = ProdutoDatabase.buscar_produto_por_id(produto_id)
    assert produto_salvo is not None
    assert produto_salvo.nome == produto_exemplo.nome

def test_excluir_produto(produto_exemplo):
    ProdutoDatabase.deletar_produto(produto_exemplo.id)
    produto_salvo = ProdutoDatabase.buscar_produto_por_id(produto_exemplo.id)
    assert produto_salvo is None  # O produto deve ter sido removido

if __name__ == "__main__":
    pytest.main()
