import customtkinter as ctk
import tkinter as tk
import bancoFuncionario as bf


# tela de cadastro de funcionarios
def cadastro_funcionario(mode:bool=0,registro:dict=None,nivel:str=None):
    # definindo testo do botão de ação
    texto_botao:str
    if not mode:texto_botao="Cadastrar"
    else:texto_botao="Atualizar"

    window=ctk.CTk()
    ctk.set_appearance_mode("dark")
    window.geometry("400x350")

    # definindo modo de operação
    if not mode:window.title('Cadastrar Funcionario')
    else:window.title('Atualizar Funcionario')

    global sucesso,nome_err,senha_err,confirm_senha_err
    sucesso=None
    nome_err=None
    senha_err=None
    confirm_senha_err=None

    window.grid_columnconfigure(0,weight=1)


    nome_input=ctk.CTkEntry(window, placeholder_text="Funcionario")
    nome_input.grid(row=0,pady=5)


    senha_input=ctk.CTkEntry(window, placeholder_text="Senha", show="*")
    senha_input.grid(row=1,pady=5)


    confirm_input=ctk.CTkEntry(window, placeholder_text="Confirme a senha", show="*")
    confirm_input.grid(row=2,pady=5)


    acesso_var=tk.StringVar(value="editor")
    opition_menu=ctk.CTkOptionMenu(window,variable=acesso_var,values=list(bf.cadastro_acesso(nivel)))
    opition_menu.grid(row=3,pady=5)


    button_cadastra=ctk.CTkButton(window, text=texto_botao, command=lambda:verifica(mode,registro))
    button_cadastra.grid(row=8,pady=5)


    # verificando se é modo de edição e inserindo dados nos campos respectivos
    if mode:
        nome_input.insert(0,registro["funcionario"])
        senha_input.insert(0,registro["senha"])
        confirm_input.insert(0,registro["senha"])


    # função que verifica se os campos são validos
    def verifica(mode,registro):
        global sucesso,nome_err,senha_err,confirm_senha_err

        # retirando mensagem de sucesso
        if sucesso is None:pass
        else: sucesso.grid_forget()


        if nome_input.get()=='':
            if nome_err is None:
                nome_err=ctk.CTkLabel(window,text="O campo Funcionario não pode ser vazio", text_color="red")
                nome_err.grid(row=4,pady=5)
            else:pass

        else:
            if nome_err is None:pass
            else:
                nome_err.grid_forget()
                nome_err=None


        if senha_input.get()=='':
            if senha_err is None:
                senha_err=ctk.CTkLabel(window,text="O campo Senha não pode ser vazio", text_color="red")
                senha_err.grid(row=5,pady=5)
            else:pass

        else:
            if senha_err is None:pass
            else:
                senha_err.grid_forget()
                senha_err=None


        if senha_input.get()!=confirm_input.get():
            if confirm_senha_err is None:
                confirm_senha_err=ctk.CTkLabel(window,text="A Senha e a confirmação devem ser iguais", text_color="red")
                confirm_senha_err.grid(row=6,pady=5)
            else:pass

        else:
            if confirm_senha_err is None:pass
            else:
                confirm_senha_err.grid_forget()
                confirm_senha_err=None

        
        if nome_err is None and senha_err is None and confirm_senha_err is None:
            if not mode:
                # inserindo dados na tabela
                entrada:dict={"funcionario":nome_input.get(),"senha":senha_input.get(),"acesso":acesso_var.get()}

                bf.insert_funcionario(entrada)

                nome_input.delete(0,tk.END)
                senha_input.delete(0,tk.END)
                confirm_input.delete(0,tk.END)


            else:
                if nome_input.get()==registro["funcionario"]:pass
                else: bf.edit_funcionario(int(registro["id"]),"funcionario",nome_input.get())

                if bf.verify_password(senha_input.get(),registro["senha"]):pass
                else: bf.edit_funcionario(int(registro["id"]),"senha",bf.hash_password(senha_input.get()))

                if acesso_var.get()==registro["acesso"]:pass
                else: bf.edit_funcionario(int(registro["id"]),"acesso",acesso_var.get())


    window.mainloop()
