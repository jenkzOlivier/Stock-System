import pytest
import sys

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

from usuario_model import Usuario

@pytest.fixture
def usuario_exemplo():
    return Usuario(user_name="teste_usuario", password="senha_teste", acesso="admin")

def test_criacao_usuario(usuario_exemplo):
    assert usuario_exemplo.user_name == "teste_usuario"
    assert usuario_exemplo.password == "senha_teste"
    assert usuario_exemplo.acesso == "admin"

def test_acesso_padrao():
    usuario = Usuario(user_name="usuario_comum", password="senha123")
    assert usuario.acesso == "editor"  # O acesso padrão deve ser "editor"

if __name__ == "__main__":
    pytest.main()
