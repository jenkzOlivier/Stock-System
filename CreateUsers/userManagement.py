import bcrypt
import json
import os

# Caminho do banco de dados
db_file = "users.json"

# Níveis de acesso
ACCESS_LEVELS = {
    "admin": "Administrador",
    "editor": "Editor",
    "viewer": "Visualizador"
}

# Garante que o arquivo users.json exista
if not os.path.exists(db_file):
    with open(db_file, "w") as f:
        json.dump({}, f)

# Função para gerar hash da senha
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

# Função para verificar senha
def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

# Carrega usuários do arquivo
def load_users():
    with open(db_file, "r") as f:
        return json.load(f)

# Salva usuários no arquivo
def save_users(users):
    with open(db_file, "w") as f:
        json.dump(users, f, indent=4)

# Garante que o admin exista
def ensure_admin():
    users = load_users()
    if "admin" not in users:
        users["admin"] = {
            "password": hash_password("admin"),
            "access": "admin"
        }
        save_users(users)

# Cria um novo usuário
def create_user(username, password, access_level):
    if not username or not password:
        return "Preencha todos os campos!", False

    users = load_users()
    
    if username in users:
        return "Usuário já existe!", False

    users[username] = {
        "password": hash_password(password),
        "access": access_level
    }
    save_users(users)
    return "Usuário criado com sucesso!", True

# Valida login
def authenticate_user(username, password):
    users = load_users()
    if username in users and verify_password(password, users[username]["password"]):
        return f"Bem-vindo, {username}! Acesso: {ACCESS_LEVELS[users[username]['access']]}", True
    return "Usuário ou senha incorretos", False

ensure_admin()
