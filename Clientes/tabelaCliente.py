import customtkinter as ctk
from tkinter import ttk
import clienteUI as cui
import bancoCliente as bc

def tabela_cliente():
    ctk.set_appearance_mode("dark")

    window=ctk.CTk()
    window.title("tabela de Clientes")

    titulo_label=ctk.CTkLabel(window,text="Campos de busca")
    titulo_label.grid(row=0,column=1,columnspan=2,pady=10)

    # campos de busca do cliente
    busca_id=ctk.CTkEntry(window, placeholder_text="Codigo")
    busca_id.grid(row=1,column=0, padx=10, pady=10)

    busca_nome=ctk.CTkEntry(window, placeholder_text="Cliente")
    busca_nome.grid(row=1,column=1, padx=10, pady=10)

    busca_end=ctk.CTkEntry(window, placeholder_text="Endereço")
    busca_end.grid(row=1,column=2, padx=10, pady=10)
    
    busca_tel=ctk.CTkEntry(window, placeholder_text="Telefone")
    busca_tel.grid(row=1,column=3, padx=10, pady=10)


    tabela=ttk.Treeview(window)
    tabela['columns']=('id','nome','endereco','telefone')

    tabela.heading("#0",text='')
    tabela.heading('id',text='COD')
    tabela.heading('nome',text='NOME')
    tabela.heading('endereco',text='END')
    tabela.heading('telefone',text='TEL')

    tabela.column('#0',width=0)
    tabela.column('id',width=50)
    tabela.column('nome',width=50)
    tabela.column('endereco',width=50)
    tabela.column('telefone',width=50)

    tabela.grid(row=2,column=1,columnspan=3)

    def busca():
        # array dos resultados
        results:list=[]
        # dicionario dos campos usados
        buscas:dict={}

        # tratamento dos campos de busca 
        try: buscas={"id":int(busca_id.get())}
        except ValueError:pass


        if busca_nome.get()=='':pass
        else: buscas.update({"nome":busca_nome.get()})
        

        if busca_end.get()=='':pass
        else: buscas.update({"endereco":busca_end.get()})


        if busca_tel.get()=='':pass
        else: buscas.update({"telefone":busca_tel.get()})


        # limpa tabela
        tabela.delete(*tabela.get_children())


        # inserindo resultados na tabela
        if buscas=={}:
            results=bc.show_clientes()

        else:
            results=bc.cliente_filter(buscas)

        for i in results:
            tabela.insert('','end',values=(i["id"],i["nome"],i["endereco"],i["telefone"]))

    busca()
    button_busca=ctk.CTkButton(window, text="Buscar", command=busca)
    button_busca.grid(row=1,column=4, padx=10, pady=10)

    button_cria=ctk.CTkButton(window, text="Adicionar", command=cui.cadastro_cliente)
    button_cria.grid(row=3,column=4,padx=10,pady=10)

    # função para abrir metodo de atualização de dados
    def update_cliente():
        try:
            # recebendo dados da tabela
            linha=tabela.selection()[0]
            dado:list=tabela.tiem(linha)['values']

            # montando dicionario para edição
            item:dict={"id":int(dado[0]),"nome":dado[1],"endereco":dado[2],"telefone":dado[3]}

            cui.cadastro_cliente(1,item)

        except IndexError:pass

    
    button_update=ctk.CTkButton(window, text="Atualizar",command=update_cliente)
    button_update.grid(row=3,column=3,padx=10,pady=10)


    def fecha():
        window.destroy()

    
    button_fecha=ctk.CTkButton(window, text="Sair",command=fecha)
    button_fecha.grid(row=3,column=0,padx=10,pady=10)
