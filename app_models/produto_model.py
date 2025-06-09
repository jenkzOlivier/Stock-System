class ProdutoModel:
    def __init__(self, id=None, nome='', marca='', descricao='', referencia='', valor=0.0, quantidade=0):
        self.id = id
        self.nome = nome
        self.marca = marca
        self.descricao = descricao
        self.referencia = referencia
        self.valor = valor
        self.quantidade = quantidade