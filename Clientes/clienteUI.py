import customtkinter as ctk
from tkinter import END
import bancoCliente as bc

# tela de cadastro de clientes
def cadastro_cliente(mode:bool=0,registro:dict=None):
    # modo de operação
    if mode:modo:str='Atualizar'
    else:modo:str='Cadastrar'


    ctk.set_appearance_mode("dark")
    window=ctk.CTk()

    # definindo modo de operação
    if not mode:window.title('Cadastrar Cliente')
    else:window.title('Atualizar Cliente')

    global sucesso, nome_err, end_err, tel_err
    sucesso=None
    nome_err=None
    end_err=None
    tel_err=None


    # campos para preenchimento
    nome_input=ctk.CTkEntry(window, placeholder_text="Cliente")
    nome_input.grid(row=0,column=0, padx=10, pady=10)

    end_input=ctk.CTkEntry(window, placeholder_text="Endereço")
    end_input.grid(row=0,column=1, padx=10, pady=10)
    
    tel_input=ctk.CTkEntry(window, placeholder_text="Telefone")
    tel_input.grid(row=0,column=2, padx=10, pady=10)

    # inserindo dados a modificar nos campos
    if mode:
        nome_input.insert(0,registro["nome"])
        end_input.insert(0,registro["endereco"])
        tel_input.insert(0,registro["telefone"])
    
    # função que verifica campos validos
    def verifica(mode,registro):
        global sucesso, nome_err, end_err, tel_err

        # retirando menssagem de sucesso
        if sucesso is None:pass
        else:sucesso.grid_forget()

        # tratamento dos dados inseridos
        if nome_input.get()=='':
            if nome_err is None:
                nome_err=ctk.CTkLabel(window,text="O campo Cliente não pode ser vazio", text_color="red")
                nome_err.grid(row=1,column=0, columnspan=3)
            else:pass

        else:
            if nome_err is None:pass
            else:
                nome_err.grid_forget()
                nome_err=None
        

        if end_input.get()=='':
            if end_err is None:
                end_err=ctk.CTkLabel(window,text="O campo Cliente não pode ser vazio", text_color="red")
                end_err.grid(row=2,column=0,columnspan=3)
            else:pass

        else:
            if end_err is None:pass
            else:
                end_err.grid_forget()
                end_err=None

        
        if tel_input.get()=='':
            if tel_err is None:
                tel_err=ctk.CTkLabel(window,text="O campo Cliente não pode ser vazio", text_color="red")
                tel_err.grid(row=3,column=0,columnspan=3)
            else:pass

        else:
            if tel_err is None:pass
            else:
                tel_err.grid_forget()
                tel_err=None


        if nome_err is None and end_err is None and tel_err is None:

            if not mode:
                # inserindo dados validos na tabela cliente
                entrada:dict={"nome":nome_input.get(), "endereco":end_input.get(), "telefone":tel_input.get()}

                bc.insert_cliente(entrada)

                nome_input.delete(0,END)
                end_input.delete(0,END)
                tel_input.delete(0,END)

                sucesso=ctk.CTkLabel(window,text="Cliente cadastrado com sucesso",text_color="green")
                sucesso.grid(row=4,column=0,columnspan=3)

        else:
            # codigo para modificar registro
            if nome_input.get==registro["nome"]:pass
            else:bc.edit_cliente(int(registro["id"]),"nome",nome_input.get())
                
            if end_input.get()==registro["endereco"]:pass
            else:bc.edit_cliente(int(registro["id"]),"endereco",end_input.get())
                
            if tel_err.get()==registro["telefone"]:pass
            else:bc.edit_cliente(int(registro["id"]),"telefone",tel_input.get())

            sucesso=ctk.CTkLabel(window,text="Cliente cadastrado com sucesso",text_color="green")
            sucesso.grid(row=4,column=0,columnspan=3)

    
    def fecha():
        window.destroy()

    
    button_cadastra=ctk.CTkButton(window, text=modo, command=lambda:verifica(mode,registro))
    button_cadastra.grid(row=5,column=2,padx=10,pady=10)

    button_fecha=ctk.CTkButton(window, text="Cancelar", command=fecha)
    button_fecha.grid(row=5,column=1,padx=10,pady=10)

    window.mainloop()
