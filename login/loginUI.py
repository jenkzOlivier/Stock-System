import os
import sys
import customtkinter as ctk
from tkinter import END
sys.path.append(os.path.join(os.path.dirname(__file__),"../menu")) # criando acesso ao folder menu
sys.path.append(os.path.join(os.path.dirname(__file__),"../Funcionarios")) # criando acesso ao folder funcionarios
import menuUI
import bancoFuncionario


def login():
    window=ctk.CTk()
    window.title("Login Seguro")
    window.geometry("400x350")

    ctk.set_appearance_mode("dark")


    label_title=ctk.CTkLabel(window, text="Acesso ao Sistema", font=("Arial", 20, "bold"))
    label_title.pack(pady=10)

    entry_user = ctk.CTkEntry(window, placeholder_text="Usuário")
    entry_user.pack(pady=5)

    entry_pass = ctk.CTkEntry(window, placeholder_text="Senha", show="*")
    entry_pass.pack(pady=5)

    btn_login = ctk.CTkButton(window, text="Login", command=lambda:acesso(entry_user.get(),entry_pass.get()))
    btn_login.pack(pady=10)

    label_result=ctk.CTkLabel(window, text="")
    label_result.pack(pady=5)


    def acesso(funcionario:str,senha:str):

        acao:dict=bancoFuncionario.login_funcionario(funcionario,senha)
        if acao["acao"]==1:
            label_result.configure(text=f"Bem-vindo, {acao["funcionario"]}!",text_color="green")
            window.destroy()
            menuUI.menu(acao["acesso"])

        else:
            label_result.configure(text="Ususario ou senha incorreta", text_color="red")
            entry_pass.delete(0,END)
            

    aviso()

    window.mainloop()



def aviso():
    # verificando se ha tabelas e credenciais cadastradas
    if bancoFuncionario.check_funcionario_table():pass
    else:
        window_warning=ctk.CTk()
        window_warning.title("ERRO DE CREDENCIAIS")
        window_warning.geometry("350x150")

        linha=ctk.CTkLabel(window_warning,text="ERRO: Usuarios não encontrados no banco",text_color="red")
        linha.pack(expand=True,anchor=ctk.CENTER)

        window_warning.mainloop()

login()