import bcrypt
import json
import os

# Configuração inicial
db_file = "users.json"
if not os.path.exists(db_file):
    with open(db_file, "w") as f:
        json.dump({}, f)

# Dicionário de níveis de acesso
ACCESS_LEVELS = {
    "admin": "Administrador",
    "editor": "Editor",
    "viewer": "Visualizador"
}

# Função para hash de senha
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Função para verificar senha
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Função para carregar usuários
def load_users():
    with open(db_file, "r") as f:
        return json.load(f)

# Função para salvar usuários
def save_users(users):
    with open(db_file, "w") as f:
        json.dump(users, f, indent=4)

# Função para criar admin se não existir
def ensure_admin():
    users = load_users()
    if "admin" not in users:
        users["admin"] = {
            "password": hash_password("admin"),
            "access": "admin"
        }
        save_users(users)

ensure_admin()