import customtkinter as ctk
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../Products"))
import tabelaProdutoUI
sys.path.append(os.path.join(os.path.dirname(__file__),"../Clientes"))
import tabelaCliente
sys.path.append(os.path.join(os.path.dirname(__file__),"../Funcionarios"))
import funcionarioUI

def menu(acesso:str):
    global nivel # acesso do usuario ao sistema
    nivel=acesso


    ctk.set_appearance_mode("dark")

    # criando uma janela com dimensões 400x350
    window=ctk.CTk()
    window.title("Menu")
    window.geometry("400x350")

    # criando botão que ira levar a janela de gerenciamento de funcionarios
    button_user=ctk.CTkButton(window, text="Funcionarios", command=lambda:funcionarioUI.cadastro_funcionario(0,None,acesso))
    button_user.pack(pady=10)

    # criando botão que leva a janela de produtos // esse nome tem de ser modificado para materiais
    button_materiais=ctk.CTkButton(window, text="Materiais", command=tabelaProdutoUI.tabela_produto)
    button_materiais.pack(pady=10)

    button_clientes=ctk.CTkButton(window, text="Clientes", command=tabelaCliente.tabela_cliente)
    button_clientes.pack(pady=10)

    window.mainloop()

