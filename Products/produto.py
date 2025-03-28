class Produto:
    def __init__(self, db, nome, quantidade, preco):
        self.db = db
        self.nome = nome
        self.quantidade = quantidade
        self.preco = preco

    def salvar(self):
        self.db.adicionar_produto(self.nome, self.quantidade, self.preco)  

    @staticmethod
    def listar_todos(db):
        produtos = db.listar_produtos() 
        return [Produto(db, nome, quantidade, preco) for _, nome, quantidade, preco in produtos]
