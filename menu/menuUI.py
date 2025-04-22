import customtkinter as ctk
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../CreateUsers")) # acessando CreateUsers folder
import userManagementUI
sys.path.append(os.path.join(os.path.dirname(__file__),"../Products"))
import tabelaProdutoUI

def menu():
    ctk.set_appearance_mode("dark")

    # criando uma janela com dimensões 400x350
    window=ctk.CTk()
    window.title("Menu")
    window.geometry("400x350")

    # criando botão que ira levar a janela de gerenciamento de funcionarios
    button_user=ctk.CTkButton(window, text="Funcionarios", command=userManagementUI.open_user)
    button_user.pack(pady=10)

    # criando botão que leva a janela de produtos // esse nome tem de ser modificado para materiais
    button_user=ctk.CTkButton(window, text="Materiais", command=tabelaProdutoUI.tabela_produto)
    button_user.pack(pady=10)

    window.mainloop()
