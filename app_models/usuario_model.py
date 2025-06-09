# usuario_model.py
class Usuario:
    def __init__(self, user_name: str, password: str, acesso: str = "editor"):
        self.user_name = user_name
        self.password = password
        self.acesso = acesso
