import pytest
import sys

import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'app_models'))
sys.path.append(os.path.join(BASE_DIR, 'data'))
sys.path.append(os.path.join(BASE_DIR, 'services'))

import bcrypt
import password_hashing 

@pytest.fixture
def senha_exemplo():
    return "senha_segura"

def test_hash_password(senha_exemplo):
    """Verifica se a função retorna um hash válido."""
    hashed = password_hashing.hash_password(senha_exemplo)
    assert isinstance(hashed, bytes)
    assert bcrypt.checkpw(senha_exemplo.encode('utf-8'), hashed)

def test_check_hashed_password(senha_exemplo):
    """Testa se a função consegue validar uma senha corretamente."""
    hashed = password_hashing.hash_password(senha_exemplo)
    assert password_hashing.check_hashed_password(senha_exemplo, hashed)

def test_senha_errada(senha_exemplo):
    """Verifica se uma senha incorreta não é validada."""
    hashed = password_hashing.hash_password(senha_exemplo)
    assert not password_hashing.check_hashed_password("senha_incorreta", hashed)

if __name__ == "__main__":
    pytest.main()
