import tkinter as tk
import customtkinter as ctk
from CreateUsers.userManagement import create_user, authenticate_user, ACCESS_LEVELS

class UserManagementApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gerenciamento de Usuários")
        self.geometry("400x350")
        ctk.set_appearance_mode("dark")

        self.label_title = ctk.CTkLabel(self, text="Cadastrar Novo Usuário", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=10)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_user.pack(pady=5)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_pass.pack(pady=5)

        self.label_access = ctk.CTkLabel(self, text="Nível de Acesso:")
        self.label_access.pack(pady=5)

        self.access_var = tk.StringVar(value="viewer")
        self.option_menu = ctk.CTkOptionMenu(self, variable=self.access_var, values=list(ACCESS_LEVELS.keys()))
        self.option_menu.pack(pady=5)

        self.btn_create = ctk.CTkButton(self, text="Criar Usuário", command=self.create_user)
        self.btn_create.pack(pady=10)

        self.label_result = ctk.CTkLabel(self, text="")
        self.label_result.pack(pady=5)

    def create_user(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        access_level = self.access_var.get()
        
        message, success = create_user(username, password, access_level)
        color = "green" if success else "red"
        self.label_result.configure(text=message, text_color=color)