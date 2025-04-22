import customtkinter as ctk
from tkinter import END
import banco_produto as bp

# tela para cadastro de produtos
def cadastro_produto(mode:bool=0,registro:dict=None):
    # modo de operação
    modo:str
    if mode:modo='Atualizar'
    else:modo='Cadastrar'


    ctk.set_appearance_mode("dark")

    window=ctk.CTk()
    # definindo modo de funcionamento
    if not mode:window.title("Cadastrar Produto")
    else:window.title("Atualizar Produto")

    # variaveis de verificação de erro
    global sucesso, nome_err, marca_err,ref_err,valor_err,quant_err
    sucesso=None
    nome_err=None
    marca_err=None
    ref_err=None
    valor_err=None
    quant_err=None


    # campos para o usuario preencher
    nome_input=ctk.CTkEntry(window, placeholder_text="Produto")
    nome_input.grid(row=0,column=0, padx=10, pady=10)

    marca_input=ctk.CTkEntry(window, placeholder_text="Marca")
    marca_input.grid(row=0,column=1, padx=10, pady=10)
    
    descricao_input=ctk.CTkEntry(window, placeholder_text="Descrição")
    descricao_input.grid(row=0,column=2, padx=10, pady=10)
    
    referencia_input=ctk.CTkEntry(window, placeholder_text="Referencia")
    referencia_input.grid(row=1,column=0, padx=10, pady=10)

    
    valor_input=ctk.CTkEntry(window, placeholder_text="Preço Unitario")
    valor_input.grid(row=1,column=1, padx=10, pady=10)
    
    quantidade_input=ctk.CTkEntry(window, placeholder_text="Quantidade")
    quantidade_input.grid(row=1,column=2, padx=10, pady=10)

    # inserindo dados nos campos para modificação do cadastro
    if mode:
        nome_input.insert(0,registro["nome"])
        marca_input.insert(0,registro["marca"])
        descricao_input.insert(0,registro["descricao"])
        referencia_input.insert(0,registro["referencia"])
        valor_input.insert(0,registro["valor"])
        quantidade_input.insert(0,registro["quantidade"])


    #função que verifica campos validos
    def verifica(mode:bool,registro:dict):
        global nome_err,marca_err,ref_err,valor_err,quant_err,sucesso

        if sucesso is None:pass
        else:
            sucesso.grid_forget()


        # fazendo tratamento de erro para cada campo validado
        if nome_input.get()=='':
            if nome_err is None:
                nome_err=ctk.CTkLabel(window, text="O campo Produto não pode ser vazio", text_color="red")
                nome_err.grid(row=2, column=0, columnspan=3)
            else:pass

        else:
            if nome_err is None:pass
            else:
                nome_err.grid_forget()
                nome_err=None

           
        if marca_input.get()=='':
            if marca_err is None:
                marca_err=ctk.CTkLabel(window, text="O campo Marca não pode ser vazio", text_color="red")
                marca_err.grid(row=3, column=0, columnspan=3)
            else:pass

        else:
            if marca_err is None:pass
            else:
                marca_err.grid_forget()
                marca_err=None

            
        if referencia_input.get()=='':
            if ref_err is None:
                ref_err=ctk.CTkLabel(window, text="O campo Referencia não pode ser vazio", text_color="red")
                ref_err.grid(row=4, column=0, columnspan=3)
            else:pass

        else:
            if ref_err is None:pass
            else:
                ref_err.grid_forget()
                ref_err=None


        try:
            float(valor_input.get())
            if valor_err is None:pass
            else:
                valor_err.grid_forget()
                valor_err=None

        except ValueError:
            if valor_err is None:
                if valor_input.get()=='':
                    valor_err=ctk.CTkLabel(window, text="Campo Preço invalido a entrada deve ser um número real usando '.' em vez de ','", text_color="red")
                    valor_err.grid(row=5, column=0, columnspan=3)

                else:pass


        try:
            int(quantidade_input.get())
            if quant_err is None:pass
            else:
                quant_err.grid_forget()
                quant_err=None

        except ValueError:
            if quant_err is None:
                if quantidade_input.get()=='':
                    quant_err=ctk.CTkLabel(window, text="Campo Quantidade invalido a entrada deve ser um número inteiro", text_color="red")
                    quant_err.grid(row=6, column=0, columnspan=3)

                else:pass


        if nome_err is None and marca_err is None and ref_err is None and valor_err is None and quant_err is None:

            # inserindo dados validados na tabela produtos
            if not mode:
                    
                    if descricao_input.get()=='':
                        # dicionario de dados para o banco de dados
                        entrada:dict={"nome":nome_input.get(), "marca":marca_input.get(), "descricao":None, "referencia":referencia_input.get(), "valor":float(valor_input.get()), "quantidade":int(quantidade_input.get())}

                    else:
                        entrada:dict={"nome":nome_input.get(), "marca":marca_input.get(), "descricao":descricao_input.get(), "referencia":referencia_input.get(), "valor":float(valor_input.get()), "quantidade":int(quantidade_input.get())}
                    
                    bp.insert_produto(entrada)

                    nome_input.delete(0,END)
                    marca_input.delete(0,END)
                    descricao_input.delete(0,END)
                    referencia_input.delete(0,END)
                    valor_input.delete(0,END)
                    quantidade_input.delete(0,END)


                    sucesso=ctk.CTkLabel(window, text="Produto cadastrado com sucesso", text_color="green")
                    sucesso.grid(row=7, column=0, columnspan=3)
            
            else:
                # codigo para modificar registro
                if nome_input.get()==registro["nome"]:pass
                else:bp.edit_produto(int(registro["id"]),"nome",nome_input.get())

                if marca_input.get()==registro["marca"]:pass
                else:bp.edit_produto(int(registro["id"]),"marca",marca_input.get())

                if descricao_input.get()==registro["descricao"]:pass
                else:bp.edit_produto(int(registro["id"]),"descricao",descricao_input.get())
                
                if referencia_input.get()==registro["referencia"]:pass
                else:bp.edit_produto(int(registro["id"]),"referencia",referencia_input.get())
                
                if int(quantidade_input.get())==registro["quantidade"]:pass
                else:bp.edit_produto(int(registro["id"]),"quantidade",int(quantidade_input.get()))
                
                if float(valor_input.get())==registro["valor"]:pass
                else:bp.edit_produto(int(registro["id"]),"valor",float(valor_input.get()))

                sucesso=ctk.CTkLabel(window, text="Produto atualizado com sucesso", text_color="green")
                sucesso.grid(row=7, column=0, columnspan=3)
                


    def fecha():
        window.destroy()

    button_cadastra=ctk.CTkButton(window, text=modo, command=lambda:verifica(mode,registro))
    button_cadastra.grid(row=8, column=2, padx=10, pady=10)

    button_fecha=ctk.CTkButton(window, text="Cancelar", command=fecha)
    button_fecha.grid(row=8, column=1, padx=10, pady=10)


    window.mainloop()
