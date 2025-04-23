import tkinter as tk
import sys
import customtkinter as ctk
import subprocess
import sqlite3
from loginDatabase import ACCESS_LEVELS, verify_password
from menu import menuUI

# Função para buscar o usuário no banco de dados
def buscar_usuario(nome):
    with sqlite3.connect("loginDatabase.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nome = ?", (nome,))
        return cursor.fetchone()

class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login Seguro")
        self.geometry("400x350")

        ctk.set_appearance_mode("dark")

        self.label_title = ctk.CTkLabel(self, text="Acesso ao Sistema", font=("Arial", 20, "bold"))
        self.label_title.pack(pady=10)

        self.entry_user = ctk.CTkEntry(self, placeholder_text="Usuário")
        self.entry_user.pack(pady=5)

        self.entry_pass = ctk.CTkEntry(self, placeholder_text="Senha", show="*")
        self.entry_pass.pack(pady=5)

        self.btn_login = ctk.CTkButton(self, text="Login", command=self.login)
        self.btn_login.pack(pady=10)

        self.label_result = ctk.CTkLabel(self, text="")
        self.label_result.pack(pady=5)

    def login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()

        usuario = buscar_usuario(username)

        if usuario:
            user_id, nome, senha_hash, nivel_acesso = usuario
            if verify_password(password, senha_hash):
                self.label_result.configure(text=f"Bem-vindo, {nome}! Acesso: {ACCESS_LEVELS[nivel_acesso]}")
                self.after(1000, self.open_user_management)
            else:
                self.label_result.configure(text="Senha incorreta", text_color="red")
        else:
            self.label_result.configure(text="Usuário não encontrado", text_color="red")

    def open_user_management(self):
        subprocess.Popen([sys.executable, "userManagementUI.py"])  # Abre UserManagementUI.py sem travar a execução
        self.destroy()  # Fecha a tela de login
        menuUI.menu()  # Abrindo a janela de menu

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
