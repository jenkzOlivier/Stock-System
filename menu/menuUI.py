import customtkinter as ctk
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../CreateUsers")) # acessando CreateUsers folder
import userManagementUI

def menu():
    ctk.set_appearance_mode("dark")

    # criando uma janela com dimensões 400x350
    window=ctk.CTk()
    window.title("Menu")
    window.geometry("400x350")

    # criando botão que ira levar a janela de gerenciamento de funcionarios
    button_user=ctk.CTkButton(window, text="funcionarios", command=userManagementUI.open_user)
    button_user.pack(pady=10)

    window.mainloop()