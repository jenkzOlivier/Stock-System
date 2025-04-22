import customtkinter as ctk
from tkinter import END
from tkinter import ttk
import produtoUI as pui
import banco_produto as bp

def tabela_produto():
    ctk.set_appearance_mode("dark")

    window=ctk.CTk()
    window.title("Tabela de Produtos")

    titulo_label=ctk.CTkLabel(window, text="Campos de Busca")
    titulo_label.grid(row=0,column=1,columnspan=2,pady=10)


    # campos de busca a produtos
    busca_id=ctk.CTkEntry(window, placeholder_text="Codigo")
    busca_id.grid(row=1,column=0, padx=10, pady=10)

    busca_nome=ctk.CTkEntry(window, placeholder_text="Nome")
    busca_nome.grid(row=1,column=1, padx=10, pady=10)

    busca_marca=ctk.CTkEntry(window, placeholder_text="Marca")
    busca_marca.grid(row=1,column=2, padx=10, pady=10)

    busca_desc=ctk.CTkEntry(window, placeholder_text="Descrição")
    busca_desc.grid(row=1,column=3, padx=10, pady=10)

    busca_ref=ctk.CTkEntry(window, placeholder_text="Referencia")
    busca_ref.grid(row=2,column=0, padx=10, pady=10)

    busca_val=ctk.CTkEntry(window, placeholder_text="Preço")
    busca_val.grid(row=2,column=1, padx=10, pady=10)

    busca_qtd=ctk.CTkEntry(window, placeholder_text="Quantidade")
    busca_qtd.grid(row=2,column=2, padx=10, pady=10)


    tabela=ttk.Treeview(window)
    tabela['columns']=('id','nome','marca','descrição','referencia','valor','quantidade')

    tabela.heading('#0',text='')
    tabela.heading('id',text='COD')
    tabela.heading('nome',text='NOME')
    tabela.heading('marca',text='MARCA')
    tabela.heading('descrição',text='DESC')
    tabela.heading('referencia',text='REF')
    tabela.heading('valor',text='PREÇO')
    tabela.heading('quantidade',text='QUANTIDADE')

    tabela.column('#0',width=0)
    tabela.column('id',width=50)
    tabela.column('nome',width=100)
    tabela.column('marca',width=100)
    tabela.column('descrição',width=100)
    tabela.column('referencia',width=100)
    tabela.column('valor',width=100)
    tabela.column('quantidade',width=100)

    tabela.grid(row=3,column=1,columnspan=2)


    def busca():
        # array dos campos de busca utilizados
        buscas:dict={}
        results:list=[]

        # tratamento dos campos de busca
        try: buscas={"id":int(busca_id.get())}
        except ValueError:pass


        if busca_nome.get()=='':pass
        else: buscas.update({"nome":busca_nome.get()})


        if busca_marca.get()=='':pass
        else: buscas.update({"marca":busca_marca.get()})


        if busca_desc.get()=='':pass
        else:buscas.update({"descricao":busca_desc.get()})


        if busca_ref.get()=='':pass
        else:buscas.update({"referencia":busca_ref.get()})


        try:buscas.update({"valor":float(busca_val.get())})
        except ValueError:pass


        try:buscas.update({"quantidade":int(busca_qtd.get())})
        except ValueError:pass


        # limpa tabela
        tabela.delete(*tabela.get_children())


        # inserindo resultados na tabela
        if buscas=={}:
            results=bp.show_produtos()
            
        else:
            results=bp.produto_filter(buscas)

        for i in results:
            if i["descricao"] is None:
                tabela.insert('','end',values=(i["id"],i["nome"],i["marca"],'',i["referencia"],i["valor"],i["quantidade"]))
            else:
                tabela.insert('','end',values=(i["id"],i["nome"],i["marca"],i["descricao"],i["referencia"],i["valor"],i["quantidade"]))

    busca()


    button_busca=ctk.CTkButton(window, text="Buscar", command=busca)
    button_busca.grid(row=2, column=3, padx=10, pady=10)

    button_cria=ctk.CTkButton(window,text="Adicionar",command=pui.cadastro_produto)
    button_cria.grid(row=4, column=3, padx=10, pady=10)

    
    # codigo para abrir o metodo de atualização de dados
    def update_produto():
        try:
            # recebendo dados da tabela
            linha=tabela.selection()[0]
            dado:list=tabela.item(linha)['values']

            # montando um dicionario para transferir dados para o metodo de edição
            item:dict={"id":int(dado[0]),"nome":dado[1],"marca":dado[2],"descricao":dado[3],"referencia":dado[4],"valor":float(dado[5]),"quantidade":int(dado[6])}

            pui.cadastro_produto(1,item)

        except IndexError:
            pass


    button_update=ctk.CTkButton(window,text="Atualizar",command=update_produto)
    button_update.grid(row=4, column=2, padx=10, pady=10)


    def fecha():
        window.destroy()


    button_fecha=ctk.CTkButton(window, text="Sair", command=fecha)
    button_fecha.grid(row=4, column=0, padx=10, pady=10)


    window.mainloop()